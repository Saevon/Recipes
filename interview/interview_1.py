#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Fills question marks ensuring there is never a run longer than the required value

Incomplete
'''

case1 = {
    "order": "?LLLLLWWWWW?????????",
    "required": 5,
    # "output": "WLLLLLLWWWWW"
}

case4 = {
    "order": "??????????WWWWW?",
    "required": 5,
    # "output": "WLLLLLLWWWWW"
}


case2 = {
    "order": "L??",
    "required": 2,
    "output": "LWW",
}


case3 = {
    "order": "W??",
    "required": 1,
    "output": False,
}


class Command(object):
    def __init__(self, char, length):
        self.char = char
        self.length = length

    def __str__(self):
        return self.char * self.length

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        if self.char == '?':
            return None
        elif self.char == 'W':
            return 1
        elif self.char == 'D':
            return 0


def compact(commands):
    resulting_command = []

    length = 0
    current_char = None
    for command in commands:
        # Compact the current chain if its ended
        if current_char != command and length != 0:
            resulting_command.append(Command(char=current_char, length=length))
            length = 0

        # Always increment by 1 since we got a new character
        length += 1

        if current_char != command:
            # Reset to the new command chain
            current_char = command

    if length != 0:
        resulting_command.append(Command(char=current_char, length=length))

    return resulting_command


def possible(nopes=0, required=0, current_val=0, is_end=False):
    # If we're in an impossible state, abort
    if current_val >= required and current_val - nopes >= required:
        return False
    elif current_val <= (-1 * required) and current_val + nopes <= (-1 * required):
        return False

    # Leave the command untouched
    if is_end:
        return True

    if (current_val == required) or current_val >= ______:
        return [
            # Account for dropping one below the
            Command(char="L", length=current_val - required),
        ]







print(compact(case1["order"]))
