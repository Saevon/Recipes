#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from scanner import *


def questor():
    print("====================")
    print("Tales of the Questor")
    scanner = DateScanner(
        path="/Users/Saevon/Documents/eBooks/Comics/Questor/",
        format="http://www.rhjunior.com/eng/wp-content/uploads/%(year)04i/%(month)02i/npc00%(comic)03i.png",
        output="%(comic)03i.png",
    )
    final = scanner.update()
    print("Final comic: ", final)


def girl_genius():
    print("====================")
    print("Girl Genius")
    scanner = DateScanner(
        path="/Users/Saevon/Documents/eBooks/Comics/Girl Genius/",
        format="http://www.girlgeniusonline.com/ggmain/strips/ggmain%(year)04i%(month)02i%(day)02i.jpg",
        output="%(comic)03i.png",
        year=2002,
        month=11,
        day=1,
        comic=1,

    )
    try:
        final = scanner.update()
    except:
        scanner.abort()
        raise

    print("Final comic: ", final)


def makeshift_miracle():
    print("====================")
    print("Makeshift Miracle")
    scanner = DateScanner(
        path="/Users/Saevon/Documents/eBooks/Comics/Makeshift Miracle/",
        format="http://cdn.makeshiftmiracle.keenspot.com/comics/mm%(year)04i%(month)02i%(day)02i.jpg",
        output="%(comic)03i.png",
        year=2011,
        month=9,
        day=26,
        comic=1,

    )
    try:
        final = scanner.update()
    except:
        scanner.abort()
        raise

    print("Final comic: ", final)


def weesh():
    print("=====")
    print("Weesh")
    scanner = DateScanner(
        path="/Users/Saevon/Documents/eBooks/Comics/Weesh/",
        format="http://weeshcomic.com/strips/%(year)04i%(month)02i%(day)02i.gif",
        output="%(comic)s.gif",
        # Starting Date
        # year=2008,
        # month=07,
        # day=14,
        year=2010,
        month=1,
        day=27,
        comic=1,
    )
    try:
        final = scanner.update()
    except:
        print("Aborting")
        scanner.abort()
        raise
    print("Final comic: ", final)


def main():
    # weesh()
    # questor()
    girl_genius()
    # makeshift_miracle()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting")

