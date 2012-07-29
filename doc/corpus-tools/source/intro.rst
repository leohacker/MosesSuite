Introduction
============

How to install
--------------
The steps to install corpus tools:

* Sync the moses suite code from github.
* Copy the folder of subproject corpus-tools to destination folder.
* Set an environment variable PYTHONPATH point to *destination*/corpustools.

Some tools, e.g. corpus clean tool, need to get support from external tools. So we need to install those
external tools and write their infos into tools configuration file. Please refer the installation
instructions for individual tool in :ref:`external corpus tools`.

List of SMT Corpus Tools
------------------------

* :ref:`moses corpus clean tool`
* :ref:`tmx2txt converter`

