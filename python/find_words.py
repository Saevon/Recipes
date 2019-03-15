import itertools
import operator

import enchant

# Spellchecker
dictionary = enchant.Dict("en_US")

if __name__ == '__main__':
    parts = [
        "v, e, m, c, j, sa, u, ch, pl, me".split(', '),
        "er, tu, a, u, oo, up, en, ra, ar, rc".split(', '),
        "to, rn, ur, n, us, es, on, rs, it, th".split(', '),
    ]

    for choices in itertools.product(*parts):
        word = reduce(operator.add, choices, '')
        if dictionary.check(word):
            print(word)
