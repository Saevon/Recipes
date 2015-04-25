#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def chunked(fh, size):
    '''
    Chunks a file handle into block of the given size
    '''
    while True:
        data = fh.read(size)
        if data == "":
            return
        yield data

