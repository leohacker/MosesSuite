# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2012, 2013, Leo Jiang
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
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
#
# Author:   Leo Jiang <leo.jiang.dev@gmail.com>

# pylint: disable=I0011,C0301,C0103,R0902,W0201,C0111

"""
Corpus Clean Config Module
"""

import codecs
import errno
import json
import logging
import os
import os.path
import sys


class CorpusCleanConfig(object):
    """Corpus clean configuration to store the info of a clean process.

    Read the clean steps from a json foramt file and store it into a list object named steps.
    Other properties should be assigned before starting corpus cleaning.

    Properties::

        steps:              a json style data to represent the clean steps.
        corpus_name:        corpus file basename.
        source_lang:        source language identifier.
        target_lang:        target language identifier.
        infile_dir:         input directory.
        working_dir:        working directory in which intermediate files are placed.
        outfile_dir:        output directory.

    Reference:
        A `sample configuration`_ of clean steps.

    .. _sample configuration: https://github.com/leohacker/MosesSuite/blob/master/src/corpus-tools/test/cleansteps.conf


    """
    def __init__(self):
        """initialize the clean config."""
        self._steps = None

    def read_cleansteps(self, filename):
        try:
            fp = codecs.open(filename, 'r', 'utf8')
            self._steps = json.load(fp)
        except IOError as e:
            print >> sys.stderr, e
            self._steps = None
        except ValueError as e:
            print >> sys.stderr, e
            self._steps = None

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, step_list):
        self._steps = step_list

    def validate_steps(self):
        """Validate the modules and the config of clean steps.

        The function would check whether can import the clean modules, and whether each module
        have the essential functions: validate, run/predicate. And it would run the function
        validate() from each module to validate the config. Return False if anything wrong.

        """
        if self._steps is None:
            print >> sys.stderr, "Failed to read the config of clean steps."
            return False

        ret = True
        for step in self._steps:
            module_name = "corpustools.clean." + step["name"]
            try:
                __import__(module_name)
            except ImportError as e:
                print >> sys.stderr, e
                ret = False
                continue

            # module must have functions: validate, run or predicate.
            module = sys.modules[module_name]
            if not hasattr(module, "validate"):
                ret = False
                continue
            elif not ( hasattr(module, "run") or hasattr(module, "predicate") ):
                ret = False
                continue

            if module.validate(step) == False:
                ret = False

        return ret

    @property
    def corpus_name(self):
        return self._corpus_name

    @corpus_name.setter
    def corpus_name(self, value):
        self._corpus_name = value

    @property
    def source_lang(self):
        return self._source_lang

    @source_lang.setter
    def source_lang(self, value):
        self._source_lang = value

    @property
    def target_lang(self):
        return self._target_lang

    @target_lang.setter
    def target_lang(self, value):
        self._target_lang = value

    @property
    def infile_dir(self):
        return self._infile_dir

    @infile_dir.setter
    def infile_dir(self, value):
        self._infile_dir = value

    @property
    def outfile_dir(self):
        return self._outfile_dir

    @outfile_dir.setter
    def outfile_dir(self, value):
        self._outfile_dir = value

    @property
    def working_dir(self):
        return self._working_dir

    @working_dir.setter
    def working_dir(self, value):
        self._working_dir = value

    def corpus_filename(self, ext=None):
        """Return corpus filename."""
        namelist = [self.corpus_name, '-'.join([self.source_lang, self.target_lang])]
        if ext is not None:
            namelist.append(ext)
        namelist.append("bitext")
        return '.'.join(namelist)

    def logger(self, ext):
        """instantiate logger for specified clean step."""
        logger = logging.getLogger(ext)     # ext name is unique for each step.
        logger.propagate = False
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename=os.path.join(self.working_dir, ext + '.log'),
                                      mode='w', encoding='utf-8', delay=True)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
