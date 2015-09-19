#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import subprocess
import os

import urllib2
import socket

from chunked import chunked


class ComicScanner(object):

    CHUNK_SIZE = 512

    def __init__(self, path):
        self.path = path

        if not os.path.exists(path):
            self.init_path()

        self._start = {
            'comic': 0,
        }

    def init_path(self):
        subprocess.check_output(['mkdir', self.path])

    def format_args(self):
        raise NotImplementedError

    def scan(self):
        '''
        Scans the filesystem returning the latest comic found
        '''
        self.comic = self._start['comic']
        while True:
            exists = os.path.isfile(self.output_file())
            if not exists:
                return self.comic
            self.comic += 1

    def output_file(self):
        '''
        Returns a path for the expected output file of the given comic number
        '''
        raise NotImplementedError

    def download_wget(self, url, output_file):
        '''
        Downloads the given url creating the given output-file with the result
            uses wget
        '''
        try:
            subprocess.check_output(["wget", url, "-O", output_file])
        except subprocess.CalledProcessError as err:
            # Wget creates an empty file if it fails
            subprocess.check_output(["rm", output_file])
            return False
        else:
            return True

    def download_urllib(self, url, output_file):
        '''
        Downloads the given url creating the given output-file with the result
            uses urllib2
        '''
        try:
            response = urllib2.urlopen(url, timeout=0.5)
        except urllib2.URLError as err:
            return False
        except socket.timeout as err:
            return False

        with open(output_file, 'w') as fh:
            for data in chunked(response, self.CHUNK_SIZE):
                fh.write(data)

        return True

    download = download_urllib


    def update(self):
        raise NotImplementedError

    # def embedded(self, search):




class DateScanner(ComicScanner):

    def __init__(self, path, format, output, year=2014, month=01, day=None, comic=0):
        super(DateScanner, self).__init__(path)

        self.format = format
        self.output = output

        self._start = {
            'year': year,
            'month': month,
            'day': day,
            'comic': comic,
        }

    def reset(self):
        self.year = self._start['year']
        self.month = self._start['month']
        self.day = self._start['day']

        self.comic = self.scan()

    def output_file(self):
        return os.path.join(self.path, (self.output % self.format_args))

    @property
    def format_args(self):
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'comic': self.comic,
        }


    def update(self):
        self.reset()

        failures = 0

        while True:
            url = self.format % self.format_args
            output_file = self.output_file()

            success = self.download(url, output_file)
            if not success:
                print 'Failed: %s:%s: %s' % (self.year, self.month, self.comic)
                failures += 1
            else:
                print "Downloaded: %s" % (self.format % self.format_args)
                self.comic += 1
                failures = 0

            self.year, self.month, self.day = next_date(self.year, self.month, self.day)

            if failures >= 12*6:
                return self.comic - 1


def next_date(year, month, day):
    if day is not None:
        if day >= 31:
            month += 1
            day = 1
        else:
            day += 1

        if month > 12:
            month = 1
            year += 1
    else:
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    return year, month, day


def questor():
    print "===================="
    print "Tales of the Questor"
    scanner = DateScanner(
        path="/Users/Saevon/Documents/eBooks/Comics/Questor/",
        format="http://www.rhjunior.com/eng/wp-content/uploads/%(year)04i/%(month)02i/npc00%(comic)03i.png",
        output="%(comic)03i.png"
    )
    final = scanner.update()
    print "Final comic: ", final

def weesh():
    print "====="
    print "Weesh"
    scanner = DateScanner(
        path="/Users/Saevon/Documents/eBooks/Comics/Weesh/",
        format="http://weeshcomic.com/strips/%(year)04i%(month)02i%(day)02i.gif",
        output="%(comic)s.gif",
        # Starting Date
        # year=2008,
        # month=07,
        # day=14,
        year=2010,
        month=01,
        day=27,
        comic=1,
    )
    final = scanner.update()
    print "Final comic: ", final

def main():
    # weesh()
    questor()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting"

