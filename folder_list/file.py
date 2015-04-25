#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import subprocess
import hashlib
import string_helpers

from chunked import chunked
from cached import cached


class File(object):

    TYPE_MUSIC = 'music'
    EXT_MUSIC = (
        '.mp3',
    )

    TYPE_MISC = 'misc'

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

    def remove(self):
        subprocess.check_call(["rm", self.path])

    def capitalize(self):
        self.rename(string_helpers.capitalize_words(self.name))

    @property
    def dir(self):
        return os.path.dirname(self.path)

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def ext(self):
        return os.path.splitext(self.path)[1]

    #########################################
    # File Types
    def type(self):
        if self.ext in File.EXT_MUSIC:
            return File.TYPE_MUSIC
        return File.TYPE_MISC

    # File Hashing

    HASH_CHUNK_SIZE = 64

    @cached
    def hash(self):
        self.__hash = hashlib.sha1()

        with open(self.path, 'r') as fh:
            for data in chunked(fh, self.HASH_CHUNK_SIZE):
                self.__hash.update(data)

        return self.__hash.hexdigest()

    def compare(self, other):
        if self.hash() == other.hash():
            return True

        return False
