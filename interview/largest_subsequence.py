#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import itertools





def largest_subsequence(input):
    # Ensure no negatives are taken, since they can never increase the sum
    input = filter(lambda x: x > 0, input)

    evens = []
    odds = []
    for val in input:
        if val % 2 == 0:
            evens.append(val)
        else:
            odds.append(val)

    odds = sorted(odds)
    if len(odds) != 0 and len(odds) % 2 == 0:
        # Drop the lowest number if we have an even number of odds
        # since: odd + odd = even
        odds = odds[1:]

    return sum(itertools.chain(odds, evens))


input = [
    -2,
    2,
    -3,
    1,
    3, 5, 3,
    4, 6, 2,
]
print largest_subsequence(input)
