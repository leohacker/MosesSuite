# -*- encoding: utf-8 -*-
# pylint: disable=C0301,C0111

import codecs
import os.path
import sys
import shutil
from subprocess import call
from corpustools.langcode import LangCode


def tokenize(clean, tools, step, lang):
    script = os.path.join(tools["stanford_segmenter.path"], 'segment.sh')
    ext = step["ext"]

    xxlang = LangCode(lang).xx_XX()
    options = step["tool"][xxlang]
    model = options["model"]
    nbest = str(options["nbest"])
    kws = options["keep_whitespace"]

    cmdline = [script, model, clean.corpus_w(lang), "UTF-8", nbest]
    if kws:
        cmdline.insert(1, "-k")

    out_fp = codecs.open(clean.corpus_w(lang, ext), 'w', 'utf-8')
    try:
        ret = call(cmdline, stdout=out_fp)
    except OSError as e:
        print e, ":", script
        sys.exit(e.errno)
    out_fp.close()

    if ret != 0:
        print "Failed to tokenzie the corpus file:", clean.corpus_w(lang)
        sys.exit(ret)

    shutil.copy(clean.corpus_w(lang, ext), clean.corpus_w(lang))
