# -*- coding: utf-8 -*-

from corpustools.clean import length_diff

def test_length_diff_01():
   source_corpus = ur'With the world focused on Iraq, North Korea, and a possible clash with Iran over nuclear weapons, Kosovo has fallen off the radar screen.'
   target_corpus = ur'Während sich die Welt auf den Irak, Nordkorea und eine mögliche Auseinandersetzung mit dem Iran über Atomwaffen konzentriert, ist der Kosovo von der Bildfläche verschwunden.'
   step = {"name": "length_diff",
           "ext" : "ldiff",
           "diff": 5,
           }
   result = length_diff.predicate(source_corpus, target_corpus, step)
   assert result == True

def test_length_diff_02():
   source_corpus = ur'With the world focused on Iraq, North Korea, and a possible clash with Iran over nuclear weapons, Kosovo has fallen off the radar screen.'
   target_corpus = ur'Während sich die Welt auf den Irak, Nordkorea und eine mögliche Auseinandersetzung mit dem Iran über Atomwaffen konzentriert.'
   step = {"name": "length_diff",
           "ext" : "ldiff",
           "diff": 5,
           }
   result = length_diff.predicate(source_corpus, target_corpus, step)
   assert result == False
