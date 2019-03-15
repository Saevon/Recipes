#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from file import File
from folder import Folder

from music_file import MusicFile


class FolderList(list):

    def __init__(self, path, recurse=False, hidden=False, show_folders=False):
        # Ensure unicode
        self.__path = unicode(path)

        # Save some flags
        self.__flag_recurse = recurse
        self.__flag_hidden = hidden
        self.__flag_folders = show_folders

        self.refresh()

    def refresh(self):
        ''' Resets the folder, grabbing the latest names and such '''
        # Clears the list, use self.clear() for python 3
        self[:] = []

        # Find all the files
        os.path.walk(self.__path, self, self.__path)

    def _to_file(self, path):
        file = File(path)
        if file.type() == File.TYPE_MUSIC:
            return MusicFile(path)
        return file

    def _to_folder(self, path):
        folder = Folder(path)
        return folder

    def __call__(self, arg, dirname, fnames):
        remove = []

        # decide which directories to keep going into
        for index, name in enumerate(fnames):
            path = os.path.abspath(os.path.join(dirname, name))

            # Decide whether to Hide any hidden files
            if not self.__flag_hidden and os.path.basename(name).startswith('.'):
                remove.append(name)
            elif os.path.isdir(name):
                # Check for any recursion
                if not self.__flag_recurse:
                    remove.append(name)

                # Also add the folders to the list if needed
                if self.__flag_folders:
                    self.append(self._to_folder(path))

            # Add the files we find
            elif os.path.isfile(path):
                self.append(self._to_file(path))

        # Now remove the filtered folders
        # Modifying this list makes os.path.walk not recurse into the given directories
        for name in remove:
            fnames.remove(name)


