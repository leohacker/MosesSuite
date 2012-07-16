# -*- encoding: utf-8 -*-
# pylint: disable=C0301,C0111

import codecs
import os.path
import shutil
import sys
from subprocess import call


def tokenize(clean, tools, step, lang):
    subdir = "tokenizer"
    moses_tokenizer = "tokenizer.perl"
    script = os.path.join(tools["moses.scripts_path"],  subdir, moses_tokenizer)
    ext = step["ext"]

    in_fp = codecs.open(clean.corpus_w(lang), 'r', 'utf-8')
    out_fp = codecs.open(clean.corpus_w(lang, ext), 'w', 'utf-8')
    try:
        ret = call([script, "-l", lang], stdin=in_fp, stdout=out_fp)
    except OSError as e:
        print e, ":", script
        sys.exit(e.errno)
    in_fp.close()
    out_fp.close()

    if ret != 0:
        print "Failed to tokenize the corpus file:", clean.corpus_w(lang)
        sys.exit(ret)

    shutil.copy(clean.corpus_w(lang, ext), clean.corpus_w(lang))
