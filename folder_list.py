#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import subprocess


def capitalize_words(name):
    ' ' .join([s.capitalize() for s in name.split(' ')])

class File(object):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.name

    def __repr__(self):
        return "'" + str(self) + "'"

    def rename(self, name):
        new_name = os.path.join(self.dir, name)
        subprocess.check_call(["mv", self.path, new_name])
        self.path = new_name

    def capitalize(self):
        self.rename(capitalize_words(self.name))

    @property
    def dir(self):
        return os.path.dirname(self.path)

    @property
    def name(self):
        return os.path.basename(self.path)


class FolderList(list):

    def __init__(self, path, recurse=False, hidden=False):
        # Save some flags
        self.__flag_recurse = recurse
        self.__flag_hidden = hidden

        # Find all the files
        os.path.walk(path, self, path)

    def __call__(self, arg, dirname, fnames):
        remove = []

        # decide which directories to keep going into
        for index, name in enumerate(fnames):
            path = os.path.abspath(os.path.join(dirname, name))

            # Decide whether to Hide any hidden files
            if not self.__flag_hidden and os.path.basename(name).startswith('.'):
                remove.append(name)

            # Check for any recursion
            elif not self.__flag_recurse and os.path.isdir(name):
                remove.append(name)

            # Add the files we find
            elif os.path.isfile(path):
                self.append(File(path))

            # TODO: possible extension code
            # _, ext = os.path.splitext(os.path.basename(name))
            # if ext in self.CONVERTED_EXTENSIONS:
            #     ext = self.CONVERTED_EXTENSIONS[ext]

            # if ext not in self.ALLOWED_EXTENSIONS:
            #     remove.append(name)
            #     continue

        # Now remove the filtered folders
        # Modifying this list makes os.path.walk not recurse into the given directories
        for name in remove:
            fnames.remove(name)


