#-*- coding: utf-8 -*-

from corpustools.config.corpusclean import CorpusCleanConfig
from nose.tools import assert_raises

class TestCorpusCleanConfig():
    def setup(self):
        self.config = CorpusCleanConfig()
        self.config.working_dir = "wdir"
        self.config.corpus_name = "corpus"
        self.config.source_lang = "en"
        self.config.target_lang = "fr"

    def test_corpus_filename(self):
        filename = self.config.corpus_filename("ext")
        assert(filename == "corpus.en-fr.ext.bitext")

    def test_corpus_filename_noext(self):
        path = self.config.corpus_filename()
        assert(path == "corpus.en-fr.bitext")
