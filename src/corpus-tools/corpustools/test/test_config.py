#-*- coding: utf-8 -*-

from corpustools.config import CorpusToolsConfig
from corpustools.config import CleanConfig
from nose.tools import assert_raises

class TestCleanConfig():
    def setup(self):
        self.config = CleanConfig()
        self.config.working_dir = "wdir"
        self.config.corpus_name = "corpus"
        self.config.source_lang = "en"
        self.config.target_lang = "fr"

    def test_corpus_w_ext(self):
        path = self.config.corpus_w("en", "ext")
        assert(path == "wdir/corpus.ext.en")

    def test_corpus_w_noext(self):
        path = self.config.corpus_w("fr")
        assert(path == "wdir/corpus.fr")

    def test_corpus_w_param_assert(self):
        assert_raises(AssertionError, self.config.corpus_w, "de")


class TestToolsConfig():
    def setup(self):
        self.config = CorpusToolsConfig()

    def testOperatorOverride(self):
        assert(self.config["moses.scripts_path"] == "/moses-suite/moses/scripts")

    def testOperatorOverrideFail01(self):
        assert(self.config["moses"] == None)

    def testOperatorOverrideFail02(self):
        assert(self.config["moses.scripts.path"] == None)

    def testOption(self):
        assert(self.config.options("moses") == ["path", "scripts_path"])

    def testOptionFail(self):
        assert(self.config.options("Moses") == None)
