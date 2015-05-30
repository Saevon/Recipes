#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from file import File
from cached import cached
from wand.image import Image


class ImageFile(File):

    def __init__(self, path):
        super(ImageFile, self).__init__(path)

    @property
    @cached
    def imagefile(self):
        return open(self.path, 'r')

    @property
    @cached
    def image(self):
        return Image(file=self.imagefile)

    def save_image(self, filename=None):
        if filename is None:
            filename = self.path

        self.image.save(filename=filename)
