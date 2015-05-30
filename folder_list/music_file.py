#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from file import File
from cached import cached

try:
    import eyed3
except ImportError:
    eyed3 = None


class MusicFile(File):

    def __init__(self, path):
        super(MusicFile, self).__init__(path)

    @property
    @cached
    def audiofile(self):
        if eyed3 is None:
            raise ImportError("No eyeD3 package, can't use 'audiofile' extension")
        return eyed3.load(self.path)

    @property
    def tag(self):
        return self.audiofile.tag
