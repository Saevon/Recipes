#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from functools import wraps


# Sentinel so that all return values are possible
_sentinel = object()


def cached(func):
    '''
    A method wrapper that caches the call after the first invocation
        This does not differentiate between different args
    '''
    data = {}

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if data.get(self, _sentinel) is _sentinel:
            data[self] = func(self, *args, **kwargs)
        return data.get(self)
    return wrapper
