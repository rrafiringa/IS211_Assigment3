#!/usr/bin/env python
# -*- Coding: utf-8 -*-

"""
Reusable url fetching module
"""

import urllib2


def fetch_url(url):
    """
    URL fetcher
    :param url: (String) URL to fetch
    :return: (string) URL data
    """
    try:
        return urllib2.urlopen(urllib2.Request(url)).read()
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print r"Could not connect to server."
            print r'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print r"The server couldn't fulfill the request."
            print r"Error code: ", e.code


def text_reader(infile, type='txt'):
    """

    :param infile:
    :param type: (String): txt | csv | byte
    :return:
    """


if __name__ == '__main__':
    DATA = fetch_url('http://www.google.com')
    print type(DATA)
