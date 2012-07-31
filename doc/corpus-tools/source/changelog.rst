ChangeLog
=========

SMT Corpus Tools 0.9
--------------------

Corpus Clean Tool 0.9

* Support predicate clean
* Support regular expression clean
* Implement lowercase in python which is faster than perl script in moses
* Implement three built-in predicate clean: lenght diff, length limit, sentence ratio.
* Internal language code converter
* Support moses tokenizer, chasen and Stanford Word Segmenter.
* Check whether number of lines of corpus is identical after tokenization.

TMX2Text Converter 1.0

* Parsing TMX file and extract the specified languages sentence align.
* Parsing all .tmx files in a directory.
* Logging the results when parsing tmx files in a directory.
* Check the number of lines in generated corpus.
