#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs=argparse.REMAINDER)
print parser.parse_args()
