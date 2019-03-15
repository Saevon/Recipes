#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from file import File
from cached import cached


eyed3 = None


class MusicFile(File):
    ''' A Music file '''

    @property
    @cached
    def _audiofile(self):
        global eyed3

        if eyed3 is None:
            try:
                import eyed3 as _eyed3
                # Save it globally
                eyed3 = _eyed3
            except ImportError:
                raise ImportError("No eyeD3 package, can't use 'audiofile' extension, call the method to try again")
        return eyed3.load(self.path)

    @property
    def audio(self):
        ''' Audio info '''
        return self._audiofile.audioinfo

    @property
    def tag(self):
        ''' Audio ID3 Tags '''
        return self._audiofile.tag
