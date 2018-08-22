#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Generates array of all DNA strands of length N
# (no cheating with itertools.permutations)

# Part 2: create a O(n) solution that can sort the generated array



DNA_LETTERS = 'ACTG'


def choose_dna():
    '''
    Generator for all DNA letters
    '''
    for dna_letter in DNA_LETTERS:
        yield dna_letter


def recurse_dna(letter_left):
    '''
    Generator that creates a dna strand of N length
    '''
    if letter_left == 0:
        return []
    elif letter_left == 1:
        # Base case for one letter, since it can't loop through and add to a zero length array
        yield from choose_dna()

    for letter in choose_dna():
        results = recurse_dna(letter_left - 1)

        for result in results:
            yield letter + result


# Note: technically better using string array
def increment_dna_point(strand, position):
    '''
    Increases the dna char at the given position

    :return:  (str, bool)  Returns a tuple with the modified strand, and whether it overflowed
    '''
    char = strand[position]
    overflow = False

    # Check if we're going to have overflow
    if char == DNA_LETTERS[-1]:
        overflow = True

    current_index = DNA_LETTERS.find(char) + 1

    # Choose the next letter
    current_index = current_index % 4

    # In case of index overflow the last part returns '' anyways
    return strand[:position] + DNA_LETTERS[current_index] + strand[position + 1:], overflow


def generate_dna(letters):
    '''
    Generator that creates a dna strand of N length
    '''

    # Base case, return no items
    if letters == 0:
        return

    # First create the starting dna strand
    strand = ''
    for i in range(letters):
        strand += DNA_LETTERS[0]

    while True:
        # Always reset the overflow:
        # We start rolling over the LAST char
        overflow = True
        overflow_position = letters - 1

        # Overflow each char
        while overflow is not False and overflow_position >= 0:
            strand, overflow = increment_dna_point(strand, overflow_position)
            if overflow is True:
                overflow_position -= 1

        yield strand

        # Base case when we overflow the entire string
        if overflow_position < 0:
            break






import unittest


class TestRecursion(unittest.TestCase):

    METHOD = staticmethod(recurse_dna)
    LIMIT = 100

    def test_zero(self):
        results = set(self.METHOD(0))

        self.assertEqual(len(results), 0)

    def test_single(self):
        results = set(self.METHOD(1))

        self.assertTrue('T' in results)
        self.assertTrue('G' in results)
        self.assertTrue('C' in results)
        self.assertTrue('A' in results)
        self.assertEqual(len(results), 4)

    def test_double(self):
        results = set(self.METHOD(2))

        self.assertTrue('GT' in results)
        self.assertTrue('AG' in results)
        self.assertTrue('AA' in results)
        self.assertEqual(len(results), 16)

    def test_triplet(self):
        results = set(self.METHOD(3))

        self.assertTrue('GTC' in results)
        self.assertTrue('AAG' in results)
        self.assertTrue('AAA' in results)
        self.assertEqual(len(results), 64)

    def test_huge(self):
        # Ensure this won't take forever to generate stuff, but still has the right values
        values = self.METHOD(self.LIMIT)

        # This assumes an existing order to them
        self.assertTrue(next(values), 'A' * self.LIMIT)
        self.assertTrue(next(values), 'A' * (self.LIMIT - 1) + 'C')
        self.assertTrue(next(values), 'A' * (self.LIMIT - 1) + 'T')


class TestGenerator(TestRecursion):
    '''
    Tests the alternative solution
    '''
    METHOD = staticmethod(generate_dna)
    LIMIT = 1000


if __name__ == '__main__':
    unittest.main()
