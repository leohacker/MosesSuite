#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=I0011,C0301,W0621

"""Loweracse module."""

import codecs


def lowercase_file(infile, outfile):
    """Read infile and write the lowercased sentences into outfile, support Unicode strings."""
    with codecs.open(infile, 'r', encoding='utf-8') as fp_in:
        with codecs.open(outfile, 'w', encoding='utf-8') as fp_out:
            lowercase_fp(fp_in, fp_out)


def lowercase_fp(fin, fout):
    """lowercase input file(fin) and output the result into output file(fout)."""
    for line_in in fin:
        line_out = line_in.lower()
        fout.write(line_out)


if __name__ == '__main__':
    import sys
    with codecs.open(sys.argv[1], 'r', encoding='utf-8') as fp_in:
        with codecs.open(sys.argv[2], 'w', encoding='utf-8') as fp_out:
            lowercase_fp(fp_in, fp_out)
