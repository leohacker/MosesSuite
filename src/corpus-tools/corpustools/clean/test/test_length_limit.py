# -*- coding: utf-8 -*-

from corpustools.clean import length_limit

class TestLengthLimit():
    def setup(self):
        self.source_corpus = ur'With the world focused on Iraq, North Korea, and a possible clash with Iran over nuclear weapons, Kosovo has fallen off the radar screen.'
        self.target_corpus = ur'Während sich die Welt auf den Irak, Nordkorea und eine mögliche Auseinandersetzung mit dem Iran über Atomwaffen konzentriert, ist der Kosovo von der Bildfläche verschwunden.'

    def test_length_limit_01(self):
        step = {"name": "length_limit",
                "ext" : "len",
                "source": [1, 24],
                "target": [1, 25]
                }
        result = length_limit.predicate(self.source_corpus, self.target_corpus, step)
        assert result == True

    def test_length_limit_02(self):
        step = {"name": "length_limit",
            "ext" : "len",
            "source": [1, 20],
            "target": [1, 20]
            }
        result = length_limit.predicate(self.source_corpus, self.target_corpus, step)
        assert result == False

    def test_length_limit_03(self):
        step = {"name": "length_limit",
                "ext" : "len",
                "source": [1, 24],
                "target": [1, 24]
                }
        result = length_limit.predicate(self.source_corpus, self.target_corpus, step)
        assert result == False
