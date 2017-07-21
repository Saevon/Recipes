#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import subprocess
import os
import json

import urllib2
import requests
import socket

from chunked import chunked
from cascade import cascade


class Latest(dict):

    def __init__(self, path):
        self.path = os.path.join(path, ".latest.txt")
        self.reset()

    @cascade
    def reset(self, data=None):
        self.clear()
        if data is not None:
            self.update(data)

    @cascade
    def load(self):
        if not os.path.exists(self.path):
            return

        with open(self.path) as fh:
            data = json.load(fh)

        if isinstance(data, dict):
            self.update(data)

    @cascade
    def save(self):
        with open(self.path, 'w') as fh:
            json.dump(dict(self), fh)


class ComicScanner(object):

    CHUNK_SIZE = 512

    def __init__(self, path, format, output):
        self.path = path
        if not os.path.exists(path):
            self.init_path()

        self.format = format
        self.output = output

        self._latest = Latest(self.path).load()

        self._start = {
            'comic': 0,
        }
        self._data = self._latest.copy()

    def init_path(self):
        subprocess.check_output(['mkdir', self.path])

    @property
    def format_args(self):
        return self._data

    def scan(self):
        '''
        Scans the filesystem returning the latest comic found
        '''
        self._data['comic'] = self._start['comic']
        while True:
            exists = os.path.isfile(self.output_file())
            if not exists:
                return self._data['comic']
            self._data['comic'] += 1

    def output_file(self):
        '''
        Returns a path for the expected output file of the given comic number
        '''
        return os.path.join(self.path, (self.output % self.format_args))

    def download_wget(self, url, output_file):
        '''
        Downloads the given url creating the given output-file with the result
            uses wget
        '''
        try:
            subprocess.check_output(["wget", url, "-O", output_file, '--max-redirect', '0'])
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
        raise NotImplementedError("urllib has redirection problems")

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

    def download_requests(self, url, output_file):
        '''
        Downloads the given url creating the given output-file with the result
            uses requests
        '''
        try:
            response = requests.get(url, allow_redirects=False, stream=True)
        except requests.exceptions.ConnectionError:
            return False

        if response.is_redirect:
            return False
        if response.status_code != 200:
            return False

        with open(output_file, 'w') as fh:
            for data in chunked(response.raw, self.CHUNK_SIZE):
                fh.write(data)

        return True


    download = download_requests


    def update(self):
        raise NotImplementedError

    def abort(self):
        self.on_abort()


    ######################
    # Events
    def on_comic_success(self):
        self._latest.reset(self._data)

    def on_comic_failure(self):
        pass

    def on_update(self):
        self._latest.save()
        self._start = self._latest.copy()

    def on_abort(self):
        pass


class SimpleScanner(ComicScanner):
    def __init__(self, path, format, output, comic=1):
        super(SimpleScanner, self).__init__(path, format, output)

    def update(self):
        success = True
        while success:
            url = self.format % self.format_args
            output_file = self.output_file()

            success = self.download(url, output_file)
            if success:
                self._data['comic'] += 1

        return self._data['comic']


class DateScanner(ComicScanner):

    def __init__(self, path, format, output, year=2014, month=01, day=None, comic=0):
        super(DateScanner, self).__init__(path, format, output)

        self._start = {
            'year': year,
            'month': month,
            'day': day,
            'comic': comic,
        }
        self._start.update(self._latest)

    def reset(self):
        self._data = self._start.copy()
        self._data['comic'] = self.scan()
        self.next_date()

    def update(self):
        self.reset()

        failures = 0

        while True:
            url = self.format % self.format_args
            output_file = self.output_file()

            success = self.download(url, output_file)
            if not success:
                print 'Failed: %(year)s:%(month)s:%(day)s %(comic)s' % self.format_args
                self.on_comic_failure()

                failures += 1
            else:
                print 'Downloaded: %(year)s:%(month)s:%(day)s %(comic)s' % self.format_args
                print "          : %s" % (self.format % self.format_args)
                self.on_comic_success()

                self._data['comic'] += 1
                failures = 0

            self.next_date()

            if failures >= 12*6:
                self.on_update()
                return self._data['comic'] - 1

    def next_date(self):
        self._data['year'], self._data['month'], self._data['day'] = next_date(self._data['year'], self._data['month'], self._data['day'])


def next_date(year, month=None, day=None):
    # increment by the proper amount (the lowest interval that is being counted)
    if day is None:
        month += 1
    elif month is None:
        year += 1
    else:
        day += 1

    # Check if the day overflowed
    if day >= 31:
        month += 1
        day = 1

    # Check if the month overflowed
    if month > 12:
        month = 1
        year += 1

    return year, month, day









def questor():
    print "===================="
    print "Tales of the Questor"
    scanner = DateScanner(
        path="/Users/Saevon/Documents/eBooks/Comics/Questor/",
        format="http://www.rhjunior.com/eng/wp-content/uploads/%(year)04i/%(month)02i/npc00%(comic)03i.png",
        output="%(comic)03i.png",
    )
    final = scanner.update()
    print "Final comic: ", final

def girl_genius():
    print "===================="
    print "Girl Genius"
    scanner = DateScanner(
        path="/Users/Saevon/Documents/eBooks/Comics/Girl Genius/",
        format="http://www.girlgeniusonline.com/ggmain/strips/ggmain%(year)04i%(month)02i%(day)02i.jpg",
        output="%(comic)03i.png",
        year=2002,
        month=11,
        day=01,
        comic=1,

    )
    try:
        final = scanner.update()
    except:
        scanner.abort()
        raise

    print "Final comic: ", final

def makeshift_miracle():
    print "===================="
    print "Makeshift Miracle"
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
    try:
        final = scanner.update()
    except:
        print "Aborting"
        scanner.abort()
        raise
    print "Final comic: ", final

def main():
    # weesh()
    # questor()
    girl_genius()
    # makeshift_miracle()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting"

