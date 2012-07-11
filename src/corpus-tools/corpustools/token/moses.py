# -*- encoding: utf-8 -*-
# pylint: disable=C0301,C0111

import codecs
import os.path
#from subprocess import call

import os
import shutil

def tokenize(clean, tools, step, lang):
    subdir = "tokenizer"
    moses_tokenizer = "tokenizer.perl"
    script = os.path.join(tools["moses.scripts_path"],  subdir, moses_tokenizer)

    # in_fp = codecs.open(clean.corpus_w(lang), 'r', 'UTF-8')
    # out_fp = codecs.open(clean.corpus_w(lang, 'tok'), 'w', 'UTF-8')
    # ret = call([script, "-l " + lang], stdin = in_fp, stdout = out_fp)
    # print ret
    # in_fp.close()
    # out_fp.close()
    cmd = script + " -l {0}".format(lang) + " < " + clean.corpus_w(lang) + " > " + clean.corpus_w(lang, 'tok')
    print cmd
    os.system(cmd)

    shutil.copy(clean.corpus_w(lang, 'tok'), clean.corpus_w(lang))
