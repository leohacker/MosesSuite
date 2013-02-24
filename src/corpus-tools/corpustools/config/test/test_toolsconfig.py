#-*- coding: utf-8 -*-

from corpustools.config.corpustools import CorpusToolsConfig


class TestCorpusToolsConfig():
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
