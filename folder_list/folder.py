#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from file import File


class Folder(File):

    def __repr__(self):
        return self.fullname

    def __init__(self, path):
        super(Folder, self).__init__(path)

    def change_ext(self, name):
        raise NotImplementedError

    def type(self):
        return File.TYPE_FOLDER

    def hash(self):
        raise NotImplementedError

    def compare(self):
        raise NotImplementedError
