# -*- encoding: utf-8 -*-
# pylint: disable=C0301,C0111

import os.path
import shutil

def tokenize(clean, tools, step, lang):
    script = os.path.join(tools["chasen.path"], 'chasen')
    rcfile = os.path.join(tools["chasen.path"], 'chasenrc')
    cmd = script + " -r " + rcfile + " -i w " + clean.corpus_w(lang) + " > " + clean.corpus_w(lang, 'tok')
    print cmd
    os.system(cmd)

    shutil.copy(clean.corpus_w(lang, 'tok'), clean.corpus_w(lang))
