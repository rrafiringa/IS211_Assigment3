#!/usr/bin/env python
# -*- Coding: utf-8 -*-

"""
IS211 - Week3 - Assignment 3
"""

import os
import re
import csv
import argparse
from urlfetch import fetch_url


DEFAULT = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'
PARSER = argparse.ArgumentParser()
PARSER.add_argument('--url', required=True, type=str, default=DEFAULT)
ARGS = PARSER.parse_args()
if ARGS.url:
    URL = ARGS.url
    FILE = os.path.basename(URL)
    try:
        with open(FILE, 'wb') as OUTFILE:
            OUTFILE.write(fetch_url(URL))
        with open(FILE, 'rb') as INFILE:
            COLS = ['path', 'datetime', 'browser', 'status', 'size']
            READER = csv.DictReader(INFILE, COLS)
            PICS = r"[A-Z-a-z-0-9-~_.\+]+(\.jpg|\.jpeg|\.gif|\.png)"
            FIREFOX = r"\bFirefox\/\d+\.\d+\b"
            CHROME = r"\bChrome\/(\d+.)+Safari\/\d+.\d+\b"
            SAFARI = r"\bVersion\/(\d+.)+Safari\/(\d+.)+\b"
            IEXPLORE = r";\sMSIE\s\d+.\d;"
            DATE = r"\b\d{4}-\d{1,2}-\d{1,2}\b"
            # Use compiled regex
            TESTS = {'image': {'regex': re.compile(PICS, re.I)},
                     'firefox': {'regex': re.compile(FIREFOX, re.I)},
                     'chrome': {'regex': re.compile(CHROME, re.I)},
                     'safari': {'regex': re.compile(SAFARI, re.I)},
                     'ie': {'regex': re.compile(IEXPLORE, re.I)}}
            DATE_MATCH = re.compile(DATE, re.I)
            # Search CSV for patterns and compile hits
            TOTAL_ENTRIES = 0
            IMAGE_HITS = 0
            BROWSER_HITS = {}
            OLD_TS = ''
            NEW_TS = ''
            for rec in READER:
                TOTAL_ENTRIES += 1
                NEW_TS = DATE_MATCH.search(rec['datetime']).group()
                if OLD_TS != NEW_TS:
                    OLD_TS = NEW_TS
                    BROWSER_HITS['firefox'] = 0
                    BROWSER_HITS['chrome'] = 0
                    BROWSER_HITS['safari'] = 0
                    BROWSER_HITS['ie'] = 0
                STRING = '{} {}'.format(rec['path'], rec['browser'])
                for idx, item in TESTS.iteritems():
                    RES = item['regex'].search(STRING)
                    if RES:
                        if idx == 'image':
                            IMAGE_HITS += 1
                        else:
                            BROWSER_HITS[idx] += 1

            print 'Total entries: ', TOTAL_ENTRIES
            IMG_STAT = (float(IMAGE_HITS)/TOTAL_ENTRIES)*100
            print 'Image requests account for {0:.2f}% of all requests.'.format(IMG_STAT)
            CTL = 0
            MAX = ''
            for brw, hits in BROWSER_HITS.iteritems():
                if hits > CTL:
                    MAX = brw.title()
                    CTL = hits
            print 'Most popular browser is {} with {} hits.'.format(MAX, CTL)

    except IOError:
        print 'IO error on file ' + FILE




