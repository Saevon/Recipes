#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import hashlib
import os
import subprocess
import tempfile
import lock

from collections import defaultdict
from shutil import rmtree

from chunked import chunked
from folder_list import File


class ParentGroup(object):

    def __init__(self, name, folder, keys, synonyms=None, hide=False):
        self.name = name
        self.folder = folder
        self.keys = keys

        if synonyms is None:
            synonyms = {}
        self.synonyms = synonyms

        self.hide = hide

    def __iter__(self):
        for key in self.keys:
            yield key
        for key in self.synonyms.keys():
            yield key

    def clean_group(self, group):
        if group is None:
            return self.name

        if group in self.synonyms.keys():
            return self.synonyms.get(group)

        return group

class TempFile(File, lock.LockMixin):

    ####################################
    # Main Usage

    def __init__(self, path, tmp=None, base=None):
        self.path = path

        self.name, self.ext = os.path.splitext(os.path.basename(path))
        self.cleaned = False

        self.tmp_folder = tmp
        if self.tmp_folder is None:
            self.set_complete()

        if "~" in self.name:
            self.group_name = self.name.split("~")[0]
            self.group_name = self.group_name.strip().title()
        else:
            self.group_name = None

        self.parent = None

        self.path_prefix = base
        if self.path_prefix is None:
            self.path_prefix = ''

    def set_parent_group(self, group):
        self.parent = group

        # Clean up the group names
        self.group_name = self.parent.clean_group(self.group_name)

    def set_complete(self):
        self.lock('no_work')

    def __str__(self):
        if self.path.startswith(self.path_prefix):
            path = self.path.replace(self.path_prefix, '/')
        else:
            path = self.path

        return '%s(%s)' % (path, self.group)


    ##########################################
    # File Movement

    def ordered_name(self, index, output):
        # If theres a parent, then remove that part from the group
        if not self.group_name:
            filename = "%03i%s" % (index, self.ext)
        else:
            filename = "%s ~ %03i%s" % (self.group_name, index, self.ext)

        # Make sure things with a parent use the proper folder, not the generic folder
        if self.parent:
            output = self.parent.folder

        return os.path.join(output, filename)

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
        subprocess.check_call(["mv", self.copy_path, self.ordered_name(index, output)])

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
            print err

    @property
    def group(self):
        if self.group_name is None:
            return None

        if self.parent:
            return "%s ~ %s" % (self.parent.name, self.group_name)

        return "%s" % (self.group_name)


class Grouper(object):

    def __init__(self, opts=None):
        self.files = []
        self.tmp = None

        self.hashes = defaultdict(list)
        self.groups = defaultdict(list)

        self.hidden_keys = set()

        if opts is None:
            self.opts = {}
        else:
            self.opts = opts
        self.opts.setdefault('no_work', True)
        self.opts.setdefault('show_dups', False)
        self.opts.setdefault('show_groups', True)
        self.opts.setdefault('edit_parents', False)
        self.opts.setdefault('parent_groups', [])
        self.opts.setdefault('base', '')

        self.parents = self.opts.get('parent_groups')

        # Map out the groups that need moving
        self.parent_keys = {}
        for parent in self.parents:
            for key in parent:
                self.parent_keys[key] = parent

    def __enter__(self):
        if not self.opts.get('no_work'):
            self.tmp = tempfile.mkdtemp()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for pic in self.files:
            pic.reset()

        if self.tmp is not None:
            rmtree(self.tmp)
        self.tmp = None

    ALLOWED_EXTENSIONS = [".jpg", ".png", ".gif"]
    CONVERTED_EXTENSIONS = {
        ".jpeg": ".jpg",
    }

    def __call__(self, arg, dirname, fnames):
        remove = []

        # decide which directories to keep going into
        for index, name in enumerate(fnames):
            # Don't recurse into hidden directories
            if os.path.basename(name).startswith('.'):
                remove.append(name)
                continue

            _, ext = os.path.splitext(os.path.basename(name))
            if ext in self.CONVERTED_EXTENSIONS:
                ext = self.CONVERTED_EXTENSIONS[ext]

            if ext not in self.ALLOWED_EXTENSIONS:
                remove.append(name)
                continue

        # Now remove the filtered files
        for name in remove:
            fnames.remove(name)

        # Now add the files to our data
        for name in fnames:
            if os.path.isdir(name):
                continue

            pic = TempFile(os.path.abspath(os.path.join(dirname, name)), tmp=self.tmp, base=self.opts['base'])

            # See if theres a parent group
            if arg is not None:
                # This has a parent, Don't mess with those folders
                pic.set_parent_group(arg)
                if not self.opts.get('edit_parents'):
                    pic.set_complete()
            elif pic.group in self.parent_keys.keys():
                # This should be added to a parent
                pic.set_parent_group(self.parent_keys.get(pic.group))

            self.add(pic)

    def add(self, pic):
        if self.opts.get('show_dups'):
            hash = pic.hash()
            self.hashes[hash].append(pic)

        self.files.append(pic)

        if pic.group is not None:
            self.groups[pic.group].append(pic)
        if pic.parent is not None and pic.parent.hide:
            self.hidden_keys.add(pic.group)

    def remove(self, file):
        self.files.remove(file)

        if file.group is not None:
            self.groups[file.group].remove(file)

    def dup_check(self):
        dups = []

        for hash, pics in self.hashes.iteritems():
            if len(pics) > 1:
                dups.append(pics)

        # Setup the return value
        if len(dups) == 0:
            return False

        return dups

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
        dups = self.dup_check()
        if dups:
            if self.opts.get('ignore_dups'):
                for group in dups:
                    for dup in group:
                        self.remove(dup)
            elif self.opts.get('slow_dups'):
                for group in dups:
                    raw_input("%s\nPress Enter: " % '\n'.join(['    ' + str(dup) for dup in group]))
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

    @staticmethod
    def __group_cmp(val1, val2):
        g1 = Grouper.__get_parent(val1)
        g2 = Grouper.__get_parent(val2)

        if g1 == g2:
            return cmp(val1, val2)
        else:
            return cmp(g1, g2)

    def print_groups(self):
        groups = set(self.groups.keys()) - self.hidden_keys

        formatted = []
        for key in sorted(groups, cmp=Grouper.__group_cmp):
            formatted.append(
                '%4i: %s' % (len(self.groups[key]), key)
            )

        print "\n".join(formatted)


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
        '-p', '--parents',
        dest='act_parent', action='store_true', default=False,
        help='Whether to touch parent folders, or leave them read-only',
    )


    parser.add_argument(
        '-n', '--dry-run',
        dest='act_dry', action='store_true', default=False,
        help='Only does side-actions (duplicates, group printing, etc.)',
    )

    parser.add_argument(
        'dirs', nargs='*', metavar='folder', help='directories to search')

    data = parser.parse_args(args)
    out = {}
    out['dirs'] = data.dirs
    out['show_groups'] = data.act_groups
    out['show_dups'] = data.act_dups
    out['ignore_dups'] = data.act_ignore_dups
    out['slow_dups'] = data.act_slow_dups
    out['edit_parents'] = data.act_parent

    out['no_work'] = data.act_dry

    return out

