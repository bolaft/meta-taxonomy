#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Name:
    importer.py

:Authors:
    Soufian Salim (soufi@nsal.im)
"""

import codecs
import doctest
import json
import function

from optparse import OptionParser


def load(opts, args):
    """
    Import a taxonomy and creates a JSON model
    """

    t_lines = codecs.open(args[0], encoding="utf-8").readlines()

    data = []
    set_name = "-"
    function = None

    for line in t_lines:
        l = line.strip()
        if l.startswith("%"):  # comment line
            pass
        elif l.startswith("!"):  # set name
            set_name = l[1:]
        elif l == "" and not function is None:  # end of function description
            data.append(function.__dict__)
            function = None
        elif l == "" and function is None:  # first empty line
            pass
        elif function is None:  # function name
            function = Function(l, set_name)
        else:  # function attribute
            function.process_attribute(l)

    with codecs.open(args[1], "w", encoding="utf-8") as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))


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
        load(options, arguments)
