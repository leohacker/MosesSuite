.. _external corpus tools:

*********************
External corpus tools
*********************

.. _corpustools config:

Corpus tools config
===================

Corpus tools configuration is a ini style file in which we can write the options for tools. The most important
option is the path of tool executable program. Other programs, e.g. corpus clean tool, can get the information of
these external tools, then call them in apropriate way.

For accessing the value, class CorpusToolsConfig support a more intuitive way, i.e. use section.option as key,
e.g. ``tools["moses.scripts_path"]``.

You can find a sample of external tools configuration file `corpustools.conf`_ from repository in which the path of
essential tools (moses scripts and two tokenizer) is configured. It's external tool's responsibility to write
the correct info into this configuration file.

.. _corpustools.conf: https://github.com/leohacker/MosesSuite/blob/master/src/corpus-tools/test/_corpustools.conf

External Tools
==============
Tokenizer
---------
For tokenization, we call some external tokenizer for specified language(s):

* The tokenizer Perl script in moses
* Stanford Word Segmenter
* Chasen Japanese Segmenter

You can download the latest release from `official website <http://nlp.stanford.edu/software/segmenter.shtml>`_
of Stanford Word Segmenter. Put them somewhere, and configure the path in corpus tools configuration. Currently
corpus tools will call the script provided by Stanford word segmenter directly.

I re-package the Chasen to simplify the compilation and support corpus files with UTF-8 encoding directly. Please
refer another sub-packages chasen-moses in project Moses Suite for detail. As this package need to be built into
binary executable, you can follow the instruction in sub-package chasen-moses to build and install it. Or following
the instruction to get a pre-compiled binary. After installing, don't forget to configure it in tools configuration.

Module API Documentation
========================

:mod:`config.corpustools_config` Module
---------------------------------------
.. automodule:: corpustools.config.corpustools_config
   :members:

:mod:`token.moses` Module
-------------------------
.. automodule:: corpustools.token.moses
   :members:

:mod:`token.stanford_segmenter` Module
--------------------------------------
.. automodule:: corpustools.token.stanford_segmenter
   :members:

:mod:`token.chasen` Module
--------------------------
.. automodule:: corpustools.token.chasen
   :members: