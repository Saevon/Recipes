#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from file import File

from music_file import MusicFile


class FolderList(list):

    def __init__(self, path, recurse=False, hidden=False):
        # Ensure unicode
        path = unicode(path)

        # Save some flags
        self.__flag_recurse = recurse
        self.__flag_hidden = hidden

        # Find all the files
        os.path.walk(path, self, path)

    def _to_file(self, path):
        file = File(path)
        if file.type() == File.TYPE_MUSIC:
            return MusicFile(path)
        return file

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
                self.append(self._to_file(path))

        # Now remove the filtered folders
        # Modifying this list makes os.path.walk not recurse into the given directories
        for name in remove:
            fnames.remove(name)


