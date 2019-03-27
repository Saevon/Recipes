'''
Reversing a string
'''

import math


def reverse(string):
    '''
    A Fun reverse "optimization" using a half-loop and letter swapping
    '''
    letters = list(string)

    # Do a half loop
    for i in range(math.floor(len(letters) / 2)):
        high = (len(letters) - 1) - i

        # Swap letters
        letters[i], letters[high] = letters[high], letters[i]

    return ''.join(letters)


print(reverse("hello"))


import re


def rev_sentence(sentence):
    '''
    A Sentence reverse, which reverses each word in the sentence
    '''
    words = []

    for match in re.finditer(r'(?P<word>\w+)(?P<suffix>\W*)', sentence):
        word = match.group('word')
        suffix = match.group('suffix')

        words.append(reverse(word))
        words.append(suffix)

    return ''.join(words)


print(rev_sentence("this is some words here, I know!    see"))
