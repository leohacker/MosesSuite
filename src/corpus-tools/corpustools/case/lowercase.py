#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# pylint: disable=C0301,C0111

import codecs
import shutil


def run(clean, tools, step):
    ext = step["ext"]
    source_corpus = clean.corpus_w(clean.source_lang)
    source_lower  = clean.corpus_w(clean.source_lang, ext)
    with codecs.open(source_corpus, 'r', encoding='utf-8') as fp_in:
        with codecs.open(source_lower, 'w', encoding='utf-8') as fp_out:
            lowercase(fp_in, fp_out)

    target_corpus = clean.corpus_w(clean.target_lang)
    target_lower  = clean.corpus_w(clean.target_lang, ext)
    with codecs.open(target_corpus, 'r', encoding='utf-8') as fp_in:
        with codecs.open(target_lower, 'w', encoding='utf-8') as fp_out:
            lowercase(fp_in, fp_out)

    shutil.copy(source_lower, source_corpus)
    shutil.copy(target_lower, target_corpus)


def lowercase(fin, fout):
    for line_in in fin:
        line_out = line_in.lower()
        fout.write(line_out)


if __name__ == '__main__':
    import sys
    with codecs.open(sys.argv[1], 'r', encoding='utf-8') as fp_in:
        with codecs.open(sys.argv[2], 'w', encoding='utf-8') as fp_out:
            lowercase(fp_in, fp_out)
