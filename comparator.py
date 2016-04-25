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

from function import Function
from optparse import OptionParser


def compare(opts, args):
    """
    Compares two taxonomies
    """

    t1 = json.loads(codecs.open(args[0], encoding="utf-8").read())
    t2 = json.loads(codecs.open(args[1], encoding="utf-8").read())

    print("parents (1 -> 2):")

    print(find_parents(t1, t2))

    print("parents (2 -> 1):")

    print(find_parents(t2, t1))

    print("equivalents:")

    print(find_equivalents(t1, t2))

    print("absent traits (1 -> 2):")

    print(find_absents(t1, t2))

    print("absent traits (2 -> 1):")

    print(find_absents(t2, t1))


def compile_attributes(t):
    attributes = []

    for f in t:
        for attribute in f["attributes"]:
            if attribute.startswith("!"):
                attribute = attribute[1:]

            if attribute not in attributes:
                attributes.append(attribute)

                if "(" in attribute:
                    start = attribute.find("(")
                    stop = attribute.rfind(")")

                    if stop - start != 2:  # avoid changing "S.provides(f)" into "S.provides(p)"
                        subattribute = attribute[start + 1:stop]

                        if "(" in subattribute:
                            # add a more general attribute
                            general_attribute = attribute.replace(subattribute, "p")  # should be more recursive than that...
                            attributes.append(general_attribute)

    return attributes


def find_absents(t1, t2):
    absents = []

    attr1 = compile_attributes(t1)
    attr2 = compile_attributes(t2)

    for a in attr1:
        if a not in attr2:
            absents.append(a)

    return absents


def find_parents(t1, t2):
    parents = {}

    for f_t1 in t1:
        for f_t2 in t2:
            if set(f_t2["attributes"]).issubset(set(f_t1["attributes"])):
                if len(f_t1["attributes"]) != len(f_t2["attributes"]):
                    if f_t2["name"] not in parents:
                        parents[f_t2["name"]] = []
                    parents[f_t2["name"]].append(f_t1["name"])

    return parents


def find_equivalents(t1, t2):
    equivalents = []

    for f_t1 in t1:
        for f_t2 in t2:
            if set(f_t2["attributes"]).issubset(set(f_t1["attributes"])):
                if len(f_t1["attributes"]) == len(f_t2["attributes"]):
                    equivalents.append((f_t1["name"], f_t2["name"]))

    return equivalents



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
        compare(options, arguments)
