#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from chunked import chunked



class ChunkedTest(unittest.TestCase):
    def setUp(self):
        super(ChunkedTest, self).setUp()

        self.file = open('tests/chunk.data', 'r')
        self.c2 = chunked(self.file, 2)
        self.c10 = chunked(self.file, 10)

    def tearDown(self):
        self.file.close()

    def testSimple(self):
        self.assertEqual(next(self.c2), '12')
        self.assertEqual(next(self.c2), '34')

    def testMultiIter(self):
        self.assertEqual(next(self.c2), '12')
        self.assertEqual(next(self.c10), '3456789012')
        self.assertEqual(next(self.c2), '34')


