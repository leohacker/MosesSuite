# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2012, Leo Jiang
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

"""Clean Config Module"""

import codecs
import errno
import json
import os
import sys
from os import path


class CleanConfig(object):
    """Class of corpus clean configuration to store the info of a clean process.

    Read the clean steps from a json foramt file and store it into a list object named steps.
    Other properties should be assigned before starting corpus cleaning.

    Properties::

        steps:              a json style data to represent the clean steps.
        corpus_name:        corpus file basename.
        source_lang:        source language identifier.
        target_lang:        target language identifier.
        infile_dir:         input corpus directory.
        working_dir:        working directory for cleanup, intermediate files are placed here.
        outfile_dir:        output corpus directory.
        log:                logger instance.

    Reference:
        A `sample configuration`_ of clean steps.

    .. _sample configuration: https://github.com/leohacker/MosesSuite/blob/master/src/corpus-tools/test/cleansteps.conf

    """
    def __init__(self, filename=None):
        """initialize the clean config with optional clean step configuration file.

        If not given clean step configuration, must assign the property steps with json style settings
        after initialization.

        :param filename:    clean step config filename.

        """
        self._steps = None
        if filename is not None:
            try:
                fp = codecs.open(filename, 'r', 'utf8')
                self._steps = json.load(fp)
            except IOError as e:
                print e
            except ValueError as e:
                print e

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, step_list):
        self._steps = step_list

    # TODO: check more situations.
    def validate_steps(self):
        return False if self._steps is None else True

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

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, value):
        self._log = value

    def validate_paths(self):
        """Check the existence of files and directories.

        Return False if any file not exists, otherwise True.
        """

        result = True

        if not path.isdir(self.infile_dir):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + self.infile_dir + "\n")
            result = False

        if not path.isdir(self.outfile_dir):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + self.outfile_dir + "\n")
            result = False

        if not path.isdir(self.working_dir):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + self.working_dir + "\n")
            result = False

        source_path = path.join(self.infile_dir, '.'.join([self.corpus_name, self.source_lang]))
        target_path = path.join(self.infile_dir, '.'.join([self.corpus_name, self.target_lang]))
        if not path.isfile(source_path):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + source_path + "\n")
            result = False
        if not path.isfile(target_path):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + target_path + "\n")
            result = False

        # TODO: a logger instance ?
        try:
            fp = open(self.log, 'w')
            fp.close()
        except IOError as e:
            print e
            result = False

        return result

    def corpus_w(self, lang, ext=None):
        """Return corpus filename after joining basename with lang and ext in working directory."""
        assert lang == self.source_lang or lang == self.target_lang
        namelist = [self.corpus_name, lang]
        if ext is not None:
            namelist.insert(1, ext)
        return path.join(self.working_dir, '.'.join(namelist))
