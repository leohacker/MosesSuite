#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2012, 2013 Leo Jiang
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Contributor:

# pylint: disable=I0011,C0301,C0103

"""Corpus Clean Tool

Clean a bitext file according to clean steps. The corpus file should be like 'path/filename.en-zhcn.bitext'.
The config file of clean steps is a json style file. A working directory as well as output directory can be
specified in command line, otherwise all intermediate result files will be put in same folder as bitext file.

Users can implement their own cleanup modules with python language, and put modules into folder "corpustools.clean".
Most of cleanup steps can be implemented as regular expression clean, some of them can be implemented as
predicate clean. Sometimes, we need to run tokenization and lowercasing in cleanup steps. These steps are implemented
by calling external tools.

Current support external tools:
    - Tokenizer : Stanford Chinese Segmentor (Chinese)
    - Tokenizer : Chasen (Japanese)
    - Tokenizer : Moses tokenizer (multilingual European languages)
    - Caser     : Moses case tool

Command line Syntax::

    Usage: clean-corpus.py [options] corpus_file clean_steps

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -c FILE, --config=FILE
                            specified corpus tools config
      -w DIR, --working-dir=DIR
                            working directory
      -o DIR, --output-dir=DIR
                            output directory

    Args:
        corpus_file:    The path to corpus file.
        clean_steps:    Configuration file of clean steps.
"""

import codecs
import errno
from itertools import izip
import logging
import os
import os.path
import shutil
import sys

from optparse import OptionParser
from corpustools.config.corpustools import CorpusToolsConfig
from corpustools.config.corpusclean import CorpusCleanConfig

__version__ = 2.0
__years__ = "2013"
__author__ = "Leo Jiang <leo.jiang.dev@gmail.com>"

def main(argv):    # pylint: disable=I0011,W0102
    """entry function."""
    corpustools_config, corpusclean_config = argv2conf(argv)
    clean_corpus(corpustools_config, corpusclean_config)


def argv2conf(argv):
    """Parse command line arguments, and construct the corpus clean and external corpus tools configuration.

    For external tools configuration, read the system-wide and user default configuration file first.
    If user give a configuration file of external tool in command line, it will be loaded also.
    A configuration file for cleanup steps must be provided as second argument in command line.

    :param argv:    command line arguments.

    :returns:
        Exit program if arguments wrong, or failed to construct configuration files. Else return a tuple,
        corpus tools configuration and cleanup configuration, (corpustools_config, corpusclean_config).

    """
    usage = "Usage: %prog [options] corpus_file clean_steps"
    num_args = 2
    version = "%prog {version} (c) {years} {author}".format(version=__version__,
                                                            years=__years__,
                                                            author=__author__
                                                            )
    # Option parser could normalize the path, i.e. expanduser and absolute the path.
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-c", "--config", metavar="FILE", dest="config",
                      type="string", help="external corpus tools config")
    parser.add_option("-w", "--working-dir", metavar="DIR", dest="working_dir",
                      type="string", help="working directory")
    parser.add_option("-o", "--output-dir", metavar="DIR", dest="output_dir",
                      type="string", help="output directory")

    (options, args) = parser.parse_args(argv[1:])
    if len(args) != num_args:
        parser.error("Too few/many arguments. Expected {num_args}".format(num_args=num_args))

    if options.config is not None:
        options.config = os.path.abspath(options.config)
        if not os.path.isfile(options.config):
            parser.error("-c --config should be followed by a corpus tools config file.")

    if options.working_dir is not None:
        options.working_dir = os.path.abspath(options.working_dir)
        if not os.path.isdir(options.working_dir):
            parser.error("-w --working-dir should be followed by an existed directory.")

    if options.output_dir is not None:
        options.output_dir = os.path.abspath(options.output_dir)
        if not os.path.isdir(options.output_dir):
            parser.error("-o --output-dir should be followed by an existed directory.")

    # corpus tools config is initialized with system and user config.
    # if specified in command line, read the config from this file. Just ignore it if failed to load.
    corpustools_config = CorpusToolsConfig()
    if options.config is not None:
        corpustools_config.readfile(options.config)

    path = args[0]
    path = os.path.abspath(path)
    steps_filename = args[1]
    steps_filename = os.path.abspath(steps_filename)

    clean_config = CorpusCleanConfig()
    clean_config.infile_dir = os.path.dirname(path)
    clean_config.outfile_dir = clean_config.infile_dir if options.output_dir is None else options.output_dir
    clean_config.working_dir = clean_config.infile_dir if options.working_dir is None else options.working_dir

    filename = os.path.basename(path)
    namelist = filename.split('.')
    if len(namelist) != 3 :
        parser.error("The corpus filename isn't correct. The pattern of filename should be filename.en-zhcn.bitext .")
    basename, langpair, ext = tuple(namelist)

    clean_config.corpus_name = basename
    [clean_config.source_lang, clean_config.target_lang] = langpair.split('-')

    clean_config.read_cleansteps(steps_filename)
    if clean_config.validate_steps() is False:
        sys.exit(errno.EINVAL)

    return (corpustools_config, clean_config)

def clean_corpus(corpustools_config, clean_config):
    """
    Clean the bitext file.

    Copy the corpus file into working directory, run the user-specified clean steps, keep the result for
    every steps, finally put the clean corpus file into output directory.

    """
    # copy the corpus into working directory.
    if not os.path.samefile(clean_config.infile_dir, clean_config.working_dir):
        shutil.copy(os.path.join(clean_config.infile_dir, clean_config.corpus_filename()), clean_config.working_dir)

    # backup the corpus to keep an original version.
    filename = os.path.join(clean_config.working_dir, clean_config.corpus_filename())
    filename_orig = os.path.join(clean_config.working_dir, clean_config.corpus_filename('orig'))
    shutil.copy(filename, filename_orig)

    # initialize root logger.
    logging.basicConfig(filename=os.path.join(clean_config.working_dir, "clean.log"),
                        filemode="w",
                        level=logging.INFO,
                        format="%(levelname)s: %(asctime)s %(message)s",
                        datefmt="%Y-%m-%d %I:%M:%S %p")

    logging.info("START cleaning corpus ...")
    # every clean step works on the bitext file except for some steps need the plain text, e.g. tokenization.
    # output corpus suffix with ext name, then copy output corpus into input corpus files for next steps.
    for step in clean_config.steps:
        logging.info("START " + step["description"])
        step["logger"] = clean_config.logger(step["ext"])

        # The module must can be imported as I had validated them in config validation.
        module_name = "corpustools.clean." + step["name"]
        __import__(module_name)

        module = sys.modules[module_name]
        if hasattr(module, 'predicate'):
            predicate_clean(clean_config, step, module.predicate)
        elif hasattr(module, 'run'):
            module.run(clean_config, corpustools_config, step)

        logging.info("END " + step["description"])

        # prepare the bitext for next step: copy the output ext version of corpus file to no ext version.
        filename_ext = os.path.join(clean_config.working_dir, clean_config.corpus_filename(step["ext"]))
        shutil.copy(filename_ext, filename)

    logging.info("END cleaning corpus.")
    # Suffix the final output with ext name 'clean'.
    filename_clean = os.path.join(clean_config.working_dir, clean_config.corpus_filename('clean'))
    shutil.copy(filename, filename_clean)

    # Copy the final cleaned corpus into output directory.
    if not os.path.samefile(clean_config.working_dir, clean_config.outfile_dir):
        shutil.copy(filename_clean, clean_config.outfile_dir)


def predicate_clean(clean_config, step, predicate):   # pylint: disable=I0011,R0914
    """Clean the corpus in a way called 'predicate clean'.

    Predicate clean can be invoked for those clean rules which only accept or drop
    the TUs from corpus according result returned by a predicate function
    (a function return True or False). Drop the align if predicate is True.

    """
    ext = step["ext"]
    filename = os.path.join(clean_config.working_dir, clean_config.corpus_filename())
    filename_ext = os.path.join(clean_config.working_dir, clean_config.corpus_filename(ext))

    infp = codecs.open(filename, 'r', encoding="UTF-8")
    outfp = codecs.open(filename_ext, 'w', encoding="UTF-8")

    lineno = 0
    droplines = 0

    # Don't use built-in function zip(). Use the iterator version izip() to avoid the MemoryError.
    for line in infp:
        lineno = lineno + 1
        if not predicate(line, step):
            outfp.write(line)
        else:
            droplines = droplines + 1
            if "log" in step and step["log"] == "lineno":
                step["logger"].info("Line {ln}".format(ln=lineno))

    logging.info("Totally {drop} lines are removed in step of {step}".format(drop=droplines, step=step["name"]))

    infp.close()
    outfp.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
