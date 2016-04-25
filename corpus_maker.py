#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
    comparator.py

:Authors:
    Soufian Salim (soufi@nsal.im)
"""

import codecs
import doctest
import json
import os
import sys

from optparse import OptionParser


def make_corpus(opts, args):
    for root, subdirs, files in os.walk(args[0]):
        list_file_path = os.path.join(root, 'my-directory-list.txt')

        with open(list_file_path, 'wb') as list_file:
            for subdir in subdirs:
                print('\t- subdirectory ' + subdir)

            for filename in files:
                file_path = os.path.join(root, filename)

                print('\t- file %s (full path: %s)' % (filename, file_path))


def parse_args():
    """
    Parses command line opts and arguments
    """

    op = OptionParser(usage="usage: %prog [opts] output_folder label")

    ########################################

    op.add_option(
        "--test",
        dest="test",
        default=False,
        action="store_true",
        help="executes the test suite")

    ########################################

    return op.parse_args()


if __name__ == "__main__":
    options, arguments = parse_args()

    ########################################

    if options.test:
        doctest.testmod()  # unit testing
    else:
        make_corpus(options, arguments)
