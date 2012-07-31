.. _moses corpus clean tool:

***********************
Moses corpus clean tool
***********************

Overview
========
A common task for SMT is cleaning up the corpus files. Clean up the long sentences and replace illegal
characters before feed the corpus files for training or creating language model in Moses system.
Furthermore, we are cleaning/replacing the strings through regular expression according to some rules
to improve the trained translation model.

Please refer :ref:`clean corpus module` module for command line syntax and :ref:`clean config` for
writing your clean steps.

Most of clean steps can be implemented as :ref:`regular expression clean`, while others can be implemented
as :ref:`predicate clean` which drop the corpus align if predicate is failed. The predicate clean way
simplified the code writing for this kind of clean.

Moses corpus clean tool is designed to be very extensible by external clean modules. User can
:ref:`write own clean module` to implement the clean step.

Some external corpus tools is needed, e.g. kinds of tokenizer or segmenter for different languages.
These external corpus tools should installed separately, and configured in
:ref:`corpus tools config <corpustools config>`.

.. _clean config:

Clean Config
============
A configuration file describe the user-defined clean steps in json format. As in json format, we can
edit this configuration file easily, add/remove steps or modify attributes for one step even
in a simple text editor.

You can find other attriubtes in the instance of CleanConfig to represent other facters in a cleaning
process, e.g. files, directories, languages etc. Please refer :ref:`clean config module` module.

Reference:
    A `sample configuration`_ of clean steps.

.. _sample configuration: https://github.com/leohacker/MosesSuite/blob/master/src/corpus-tools/test/cleansteps.conf

Clean Steps
===========

.. _regular expression clean:

Regular Expression Clean
------------------------
Most of cleanup are deleting strings or replacing strings in align sentences. User can specify regular
expression in configuration. A typical regex clean step should include ``description``, ``action``, ``pattern``
at least. The value of action can be ``delete_line``, ``delete`` or ``replace``. If action is replace,
``repl`` is needed. pattern is a regular expression, but in json format every backslash should be escaped,
e.g. write the regex ``\d`` as ``\\d`` in json cofiguration. The only character '\' need to be escaped.

The additional option can be specified:

- ``apply_to`` indicate which sentence should be cleaned, default Both.
- ``unicode`` indicate regular expression is unicode awareness. default false.
- ``case_insensitive`` indicate whether search is case sensitive or not, default false(sensitive).

.. code-block:: guess

    {
      "description": "integer",
      "action": "replace",
      "pattern" : "\\d+",
      "repl" : "num",
      "apply_to": "source",
      "unicode": true,
      "case_insensitive": true
    }

.. _predicate clean:

Predicate Clean
---------------
Now we have the following predicate clean modules built in. In predicate clean module,
the function ``predicate`` must be implemented. Please refer :ref:`predicate clean modules` for signatures
of these functions.

- clean align beyond the length limit.
- clean wrong sentence ratio align
- clean length diff align

.. _write own clean module:

Write own clean module
----------------------
You can write own clean module to extend the corpus clean tool to support new clean rules. The new clean module
should be put into the sub-package ``corpustools.clean``, and have an entry function `run(clean, tools, step)`.
You can get whole clean information from clean configuration, and get external corpus tools from tools configuration.
The parameter step indicate the configuration for current step. Please refer the source code for example.

For predicate clean, corpus corpus tool had implemented the common code, so you only need to provide a function
to return True or False according to current sentence align. Also please refer the built-in modules for example.


Module API Documentation
========================

.. _clean corpus module:

:mod:`clean_corpus` Module
--------------------------
.. automodule:: corpustools.clean_corpus
   :members:
   :member-order: bysource

.. _clean config module:

:mod:`config.clean_config` Module
---------------------------------
.. automodule:: corpustools.config.clean_config
   :members:

:mod:`clean.regex` Module
-------------------------
.. automodule:: corpustools.clean.regex
   :members:
   :member-order: bysource

.. _predicate clean modules:

predicate clean
---------------
.. autofunction:: corpustools.clean.length_diff.predicate
.. autofunction:: corpustools.clean.length_limit.predicate
.. autofunction:: corpustools.clean.sentence_ratio.predicate

:mod:`clean.tokenize` Module
----------------------------
.. automodule:: corpustools.clean.tokenize
   :members:
   :member-order: bysource

:mod:`clean.lowercase` Module
-----------------------------
.. automodule:: corpustools.clean.lowercase
   :members:
   :member-order: bysource