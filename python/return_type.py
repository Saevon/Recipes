#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from functools import wraps


def return_type(Type):
    '''
    A decorator that updates the return type to the given type
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return Type(func(*args, **kwargs))
        return wrapper
    return decorator
