#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from cached import cached


class CachingClass(object):

    def __init__(self, arg=None):
        self.arg = arg

    @property
    @cached
    def test(self):
        self.arg += 1
        return self.arg


class CachedTest(unittest.TestCase):
    def setUp(self):
        super(CachedTest, self).setUp()

        self.one = CachingClass(9)
        self.two = CachingClass(3)

    def testCache(self):
        # The value should remain constant
        # .: the function is only called once
        self.assertEqual(self.one.test, 10)
        self.assertEqual(self.one.test, 10)

        # The second object should have its own
        # unique value
        self.assertEqual(self.two.test, 4)


