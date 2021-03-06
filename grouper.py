#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import hashlib
import itertools
import os
import re
import subprocess
import tempfile

from collections import defaultdict
from shutil import rmtree

import lock
from chunked import chunked
from folder_list import File
from grouper_lib.group_dict import GroupDict
from grouper_lib.parent import ParentFinder, ParentGroup


class TempFile(File, lock.LockMixin):
    '''
    A file that knows about its current sorting, and what it should be renamed too
    It has safety checks so it can undo half-way sorted files (in case of an abort)
    '''

    ####################################
    # Main Usage
    def __init__(self, path, tmp=None, base=None):
        # Defaults
        self.group_name = ''
        self.prefix = ''
        self.copy_path = None

        self.path = path

        self.cleaned = False

        self.tmp_folder = tmp
        if self.tmp_folder is None:
            self.set_complete()

        self.load_details()

        self.parent = None

        self.path_prefix = base
        if self.path_prefix is None:
            self.path_prefix = ''

    #-------------------------------------------------------------------
    # File Identification

    PATH_REGEX = re.compile(
        r'((?P<prefix>[A-Za-z ]+) *~ *)?'
        r'(?P<group>[A-Za-z ]+) *~ *'
        r'('
            # "Batch" format allows you to group similar files
            r'('
                r'(?P<batch>[A-Za-z ]+)'
                r'\s*\.\s*'
                r'(?P<index>[0-9]+)'
            r')'
        r'|'
            # Its a sorted value
            r'(?P<sorted>[0-9]+)'
        r'|'
            # Otherwise its just randomness, aka needs to be numbered
            r'(?P<random>[^\.~]+)'
        r')'
        r'$'
    )

    @classmethod
    def is_valid(_class, name):
        '''
        Checks if the filename is a valid groupable file
        '''
        match = _class.PATH_REGEX.match(name)
        return match is not None

    def load_details(self):
        '''
        Figures out the group this should be under
        '''
        match = self.PATH_REGEX.match(self.name)
        if match is None:
            self.group_name = None

            return

        self.prefix = match.group('prefix')
        if self.prefix is not None:
            self.prefix = self.prefix.strip()

        self.group_name = match.group('group').strip().title()

        # Identify the type of object
        self.batch = match.group('batch')
        if self.batch is not None:
            self.batch = self.batch.strip()

        # Random value ones are just sortec
        if self.batch is None:
            return

        self.index = int(match.group('index').strip())

    def set_parent_group(self, parent, is_sorted=False):
        self.parent = parent
        if is_sorted:
            self.prefix = parent.prefix

        # Convert the group names to how the parent wants them
        # (aliases, styles, etc)
        self.group_name = self.parent.clean_group(self.group_name)

    def output_filename(self, index, output):
        '''
        Generates the output filename
        '''
        filename = ''

        # Having a group is higher priority than having just a prefix
        if self.group_name is not None:
            filename += self.group_name + ' ~ '
        else:
            # Prefix is similar, but its for index only ones
            filename += self.prefix + ' ~ '

        # Format by type
        if self.batch is not None:
            filename += '%s.%03i' % (self.batch, self.index)
        else:
            filename += '%03i' % index

        # add the final extension
        filename += self.ext

        # Make sure things with a parent use the proper folder, not the generic folder
        if self.parent:
            output = self.parent.folder

        return os.path.join(output, filename)

    @property
    def group(self):
        '''
        Returns the unique group it should be in
        '''
        parts = []

        if self.prefix is not None:
            parts.append(self.prefix)
        elif self.parent is not None:
            parts.append(self.parent.name)

        if self.group_name != self.parent.name:
            parts.append(self.group_name)

        hash_string = ' ~ '.join(parts)

        return hash_string

    @property
    def indexed_group(self):
        '''
        Returns the indexed group name (inluding the batch), only works on is_pre_sorted items
        '''
        return self.group + ' ~ ' + self.batch

    @property
    def is_pre_sorted(self):
        return self.batch is not None


    def __str__(self):
        if self.path.startswith(self.path_prefix):
            path = self.path.replace(self.path_prefix, '/')
        else:
            path = self.path

        return '%s(%s)' % (path, self.group_name)


    ##########################################
    # File Movement


    def set_complete(self):
        '''
        Marks the file as "already moved"
        '''

        # Ensure the file will never get moved
        self.lock('no_work')

    @lock.when_unlocked('no_work')
    def tmp_move(self):

        # Create the temporary file copy
        fh = tempfile.NamedTemporaryFile(dir=self.tmp_folder, delete=False)
        self.copy_path = fh.name
        fh.close()

        subprocess.check_call(["cp", self.path, self.copy_path])

        # Mark that we've done the actual work
        # And that it might need undoing
        # Right before we do an irreversible change
        self.lock('can_reset')

        # remove the original file
        subprocess.call(["rm", self.path])

    @lock.when_unlocked('no_work')
    @lock.when_locked('can_reset')
    def move(self, index, output):
        '''
        Moves the file to its final destination
        '''
        output_filename = self.output_filename(index, output)
        if os.path.exists(output_filename):
            raise Exception("File already exists: {}".format(output_filename))

        subprocess.check_call(["mv", self.copy_path, output_filename])

        # Mark that we've finished processing the file, thus there is nothing more to reset
        self.unlock('can_reset')

    @lock.when_unlocked('no_work')
    @lock.when_locked('can_reset')
    def reset(self):
        '''
        Reset any changes to the file (cleanup operation in case of error)
        '''
        try:
            subprocess.check_call(["mv", self.copy_path, self.path])
        except subprocess.CalledProcessError as err:
            print(err)
            raise Exception("Failed to move {} to {}".format(self.copy_path, self.path))


class Grouper(object):

    def __init__(self, opts=None):
        self.files = []
        self.tmp = None

        self.hashes = defaultdict(list)
        self.groups = GroupDict()

        self.hidden_keys = set()

        if opts is None:
            self.opts = {}
        else:
            self.opts = opts
        self.opts.setdefault('parent_groups', [])
        self.opts.setdefault('base', '')

        self.parents = self.opts.get('parent_groups')

        self.errors = set()

        # Map out the groups that need moving
        self.parent_finder = ParentFinder()
        for parent in self.parents:
            self.parent_finder.add(parent)

    def __enter__(self):
        if not self.opts.get('no_work'):
            self.tmp = tempfile.mkdtemp()
            print("Tmp Folder: %s" % self.tmp)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        broke = False

        for pic in self.files:
            try:
                pic.reset()
            except Exception as error:
                print(error)
                broke = True

        # Don't remove all the tmp files if some of them didn't revert correctly
        if not broke and self.tmp is not None:
            rmtree(self.tmp)
        self.tmp = None

    ALLOWED_EXTENSIONS = [".jpg", ".png", ".gif"]
    CONVERTED_EXTENSIONS = {
        ".jpeg": ".jpg",
    }

    def __call__(self, arg, dirname, fnames):
        remove = []

        # decide which directories to keep going into
        for index, filename in enumerate(fnames):
            # Don't recurse into hidden directories
            if os.path.basename(filename).startswith('.'):
                remove.append(filename)
                continue

            # Convert extension aliases
            name, ext = os.path.splitext(os.path.basename(filename))
            if ext in self.CONVERTED_EXTENSIONS:
                ext = self.CONVERTED_EXTENSIONS[ext]

            # Filter out disallowed extensions
            if ext not in self.ALLOWED_EXTENSIONS:
                remove.append(filename)
                continue

            # Also filter out invalid files
            if not TempFile.is_valid(name):
                remove.append(filename)
                continue

        # Now remove the filtered files
        for name in remove:
            fnames.remove(name)

        # Now add the files to our data
        for name in fnames:
            if os.path.isdir(name):
                continue

            fullpath = os.path.abspath(os.path.join(dirname, name))
            pic = TempFile(fullpath, tmp=self.tmp, base=self.opts['base'])

            # See if theres a parent group
            parent = arg
            if parent is not None:
                # This has a parent, Don't mess with those folders
                pic.set_parent_group(arg, is_sorted=True)

                if not self.opts.get('edit_parents'):
                    pic.set_complete()
            else:
                parent = self.parent_finder.find(pic)
                if parent is None:
                    if not self.opts.get('ignore_invalid_filename'):
                        self.errors.add('No Parent for: %s' % (fullpath))
                    continue
                pic.set_parent_group(parent)

            # Check to make sure the rules for this parentGroup is followed
            error = parent.check_validity(pic)
            if error is not None:
                if not self.opts.get('ignore_invalid_filename'):
                    self.errors.add('Invalid file for parent(%s): %s (%s)' % (parent, fullpath, error))
                continue

            self.add(pic)

    def add(self, pic):
        if self.opts.get('show_dups'):
            hash = pic.hash()
            self.hashes[hash].append(pic)

        self.files.append(pic)

        # Find out whether the group is displayable
        is_hidden = False
        if pic.parent is not None and pic.parent.hide:
            is_hidden = True

        self.groups.add(pic, is_hidden)

    def remove(self, file):
        self.files.remove(file)

        self.groups.remove(file)

    def dup_check(self):
        dups = []

        for hash, pics in self.hashes.iteritems():
            if len(pics) > 1:
                dups.append(pics)

        # Setup the return value
        if len(dups) == 0:
            return False

        return dups

    def dup_input(self, choices):
        print("Duplicates found (Keep which one?)")
        PREVIEW_RE = re.compile("p *([0-9]+)")

        while True:
            print('  i: ignore this group')
            print('  p#: open image in finder')
            print('\n'.join(['  %i: %s' % (index, choice) for index, choice in enumerate(choices)]))
            inp = raw_input('\n>> ')

            match = PREVIEW_RE.match(inp)
            if match:
                choice = choices[int(match.group(1))]
                subprocess.call(["open", "-R", choice.path])
                continue

            # Try to get a number out
            try:
                inp = int(inp)
            except ValueError:
                pass

            if inp == 'i':
                inp = None
                break
            elif inp >= 0 and inp < len(choices):
                break
            else:
                print("Invalid Input")

        # If the user ignores the dups
        # then mark them as ignored
        if inp is None:
            for dup in choices:
                self.remove(dup)
            return

        # If there was a choice, delete the rest
        for idx, dup in enumerate(choices):
            if idx == inp:
                continue

            # delete the file
            dup.remove()

            self.remove(dup)

    def walk(self, folders, output):
        # If we're not doing any real work, then yay! no checks needed
        if not self.opts.get('no_work'):
            # Ensure everything about to happen is legal
            if self.tmp is None:
                raise Exception("Needs to be called in a 'with Grouper():' call")

            if not os.path.exists(output) or not os.path.isdir(output):
                raise Exception("Invalid Output folder: %s", output)

        # Find any parent folders first
        for parent in self.parents:
            os.path.walk(parent.folder, self, parent)

        # Find all the files
        for folder in folders:
            os.path.walk(folder, self, None)

        # Now check if there were any problems
        if not self.groups.is_valid() and not self.opts.get('ignore_invalid_batches'):
            for group, reason in self.groups.invalid_groups():
                self.errors.add("Duplicate Group Index (%s): %s" % (
                    group, [file.path for file in reason]
                ))

        if len(self.errors):
            raise Exception('Errors:' + ''.join(['\n    ' + error for error in self.errors]))

        dups = self.dup_check()
        if dups:
            if self.opts.get('ignore_dups'):
                for group in dups:
                    for dup in group:
                        self.remove(dup)
            elif self.opts.get('slow_dups'):
                for group in dups:
                    self.dup_input(group)
            else:
                groups = []
                for group in dups:
                    groups.append(', '.join([str(dup) for dup in group]))
                raise Exception("Duplicate Files: were found: \n    %s" % '\n    '.join(groups))


        # Check if we're doing work again
        if not self.opts.get('no_work'):
            # First remove the original files (They'll be in the way)
            for pic in self.files:
                pic.tmp_move()

            # Now move the temp files to the sorted location
            for group, files in self.groups.iteritems():
                if group is None:
                    continue

                index = 1

                for pic in files:
                    # Move the file to its final destination
                    pic.move(index, output)

                    index += 1

        if self.opts.get('show_groups'):
            self.print_groups()

    @staticmethod
    def __get_parent(val):
        if "~" in val:
            return val.split("~")[0]
        return None

    def print_groups(self):
        group_names = self.groups.visible_groups()

        formatted = []
        for key in sorted(group_names):
            formatted.append(
                '%4i: %s' % (self.groups.get_count(key), key)
            )

        print("\n".join(formatted))




import argparse

def parse(args=None):
    parser = argparse.ArgumentParser(description='Groups up image files', prog='grouper')
    parser.add_argument(
        '-g', '--groups',
        dest='act_groups', action='store_true', default=False,
        help='shows the groups found',
    )
    parser.add_argument(
        '-d', '--dups',
        dest='act_dups', action='store_true', default=False,
        help='checks for duplicates',
    )
    parser.add_argument(
        '-s', '--slow-dups',
        dest='act_slow_dups', action='store_true', default=False,
        help='Shows duplicates one by one, waiting for input before continuing',
    )
    parser.add_argument(
        '--ignore-dups',
        dest='act_ignore_dups', action='store_true', default=False,
        help='Whether to ignore duplicates, not doing anything to them',
    )
    parser.add_argument(
        '--ignore-batch',
        dest='act_ignore_batch', action='store_true', default=False,
        help='Whether to ignore invalid batches, not doing anything to them',
    )
    parser.add_argument(
        '--ignore-filename',
        dest='act_ignore_filename', action='store_true', default=False,
        help='Whether to ignore invalid filenames (ones that match the format, but are not part of the parent groups), not doing anything to them',
    )
    parser.add_argument(
        '-i',
        dest='act_ignore_errors', action='store_true', default=False,
        help='Whether to ignore all problems',
    )

    parser.add_argument(
        '-p', '--parents',
        dest='act_parent', action='store_true', default=False,
        help='Whether to touch parent folders, or leave them read-only',
    )

    parser.add_argument(
        '-n', '--dry-run',
        dest='act_dry', action='store_true', default=False,
        help='Only does side-actions (duplicates, group printing, etc.)',
    )

    data = parser.parse_args(args)
    out = {}
    out['show_groups'] = data.act_groups
    out['show_dups'] = data.act_dups
    out['ignore_dups'] = data.act_ignore_dups
    out['ignore_invalid_batches'] = data.act_ignore_batch
    out['ignore_invalid_filename'] = data.act_ignore_filename

    if data.act_ignore_errors is True:
        out['ignore_dups'] = True
        out['ignore_invalid_batches'] = True
        out['ignore_invalid_filename'] = True

    out['slow_dups'] = data.act_slow_dups
    if out.get('slow_dups') is True:
        out['show_dups'] = True
    out['edit_parents'] = data.act_parent

    out['no_work'] = data.act_dry

    return out

