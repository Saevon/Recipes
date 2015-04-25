#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def capitalize_words(string):
    '''
    Capitalizes every word in the string
    '''
    ' ' .join([s.capitalize() for s in string.split(' ')])
