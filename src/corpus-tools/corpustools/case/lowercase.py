#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0301,C0111

import codecs
import shutil


def run(clean, tools, step):
    ext = step["ext"]
    lowercorpus(clean, clean.source_lang, ext)
    lowercorpus(clean, clean.target_lang, ext)


def lowercorpus(clean, lang, ext):
    corpus = clean.corpus_w(lang)
    corpus_lc = clean.corpus_w(lang, ext)
    with codecs.open(corpus, 'r', encoding='utf-8') as fp_in:
        with codecs.open(corpus_lc, 'w', encoding='utf-8') as fp_out:
            lowercase(fp_in, fp_out)

    shutil.copy(corpus_lc, corpus)


def lowercase(fin, fout):
    for line_in in fin:
        line_out = line_in.lower()
        fout.write(line_out)


if __name__ == '__main__':
    import sys
    with codecs.open(sys.argv[1], 'r', encoding='utf-8') as fp_in:
        with codecs.open(sys.argv[2], 'w', encoding='utf-8') as fp_out:
            lowercase(fp_in, fp_out)
