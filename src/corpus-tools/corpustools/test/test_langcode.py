#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from nose.tools import assert_raises
from nose.tools import raises
from corpustools.langcode import LangCode


class TestLangCode:
    def check_constructor(self, param, value):
        lc = LangCode(param)
        assert lc._langcode == value

    def test_constructor(self):
        params = ["eng", "Chinses", "AB_AE",
                  "en_US", "zh_cn", "zh",    "EN-US",
                  "zh-CN.gbk", "en_US.UTF-8"]
        result = [None, None, None,
                  "en_US", "zh_CN", "zh_CN", "en_US", 
                  "zh_CN", "en_US"]
        for param, value in zip(params, result):
            yield self.check_constructor, param, value

    def test_xx(self):
        lc = LangCode("en-US")
        assert lc.xx() == "en"

    def test_xx_XX(self):
        lc = LangCode("zh_tw")
        assert lc.xx_XX() == "zh_TW"

    def test_TMX_form(self):
        lc = LangCode("zh_CN")
        assert lc.TMX_form() == "ZH-CN"
