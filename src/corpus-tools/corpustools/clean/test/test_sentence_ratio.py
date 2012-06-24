#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from corpustools.clean import sentence_ratio

def test_sentence_ratio_01():
   source_corpus = ur'With the world focused on Iraq, North Korea, and a possible clash with Iran over nuclear weapons, Kosovo has fallen off the radar screen.'
   target_corpus = ur'Während sich die Welt auf den Irak, Nordkorea und eine mögliche Auseinandersetzung mit dem Iran über Atomwaffen konzentriert, ist der Kosovo von der Bildfläche verschwunden.'
   step = {"name": "sentence_ratio",
           "ext" : "ratio",
           "ratio": 9
           }
   result = sentence_ratio.predicate(source_corpus, target_corpus, step)
   assert result == True

def test_sentence_ratio_02():
   source_corpus = ur'With the world focused on Iraq, North Korea, and a possible clash with Iran over nuclear weapons, Kosovo has fallen off the radar screen.'
   target_corpus = ur'Während sich'
   step = {"name": "sentence_ratio",
           "ext" : "ratio",
           "ratio": 9
           }
   result = sentence_ratio.predicate(source_corpus, target_corpus, step)
   assert result == False
