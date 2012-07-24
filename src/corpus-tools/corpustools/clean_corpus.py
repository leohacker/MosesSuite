#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=I0011,C0301,C0103

"""Moses Corpus Clean Tool

Clean the aligned corpus files according to user specified configuration. Most of cleanup can be implemented as
regular expression clean, some of them can be implemented as predicate clean. Generally, we would
run tokenization and lowercasing on corpus files also.

Command line Syntax::

    Usage: clean-corpus.py [options] corpus_directory corpus_basename source_lang target_lang clean_step_config

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -c FILE, --config=FILE
                            specified corpus tools config
      -w DIR, --working-dir=DIR
                            working directory
      -o DIR, --output-dir=DIR
                            output directory
      -l FILE, --log=FILE   log file

    Args:
        corpus_directory:   Directory in which corpus files are placed.
        corpus_basename:    Basename of corpus files, e.g. corpus is the basename of file corpus.en.
        source_lang:        Source corpus language, for example 'en'.
        target_lang:        Target corpus language, for example 'zh'.
        clean_step_config:  Configuration file for clean steps.
"""

import codecs
import errno
import shutil
import sys
from os import path

from optparse import OptionParser
from corpustools.config.corpustools_config import CorpusToolsConfig
from corpustools.config.clean_config import CleanConfig


def main(argv):    # pylint: disable=I0011,W0102
    """entry function."""
    tools_config, clean_config = argv2conf(argv)
    clean_corpus(tools_config, clean_config)


def argv2conf(argv):
    """
    Parse command line arguments, construct configurations for clean and tools.

    Parse the commandline arguments, construct clean config and tools config if specified.
    If not specify the tools config in command line, read the system and user default settings.

    Args
        :argv: command line arguments.

    Returns
        :(tools_config, clean_config): A tuple of tools configuration and clean configuration.

    """
    usage = "Usage: %prog [options] corpus_directory corpus_basename source_lang target_lang clean_step_config"
    num_args = 5
    version = "%prog 0.8 (c) 2012 Leo Jiang <leo.jiang.dev@gmail.com>"
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-c", "--config", metavar="FILE", dest="config",
                      type="string", help="specified corpus tools config")
    parser.add_option("-w", "--working-dir", metavar="DIR", dest="working_dir",
                      type="string", help="working directory")
    parser.add_option("-o", "--output-dir", metavar="DIR", dest="output_dir",
                      type="string", help="output directory")
    parser.add_option("-l", "--log", metavar="FILE", dest="log",
                      type="string", help="log file")

    (options, args) = parser.parse_args(argv[1:])
    if len(args) != num_args:
        parser.error("Too few/many arguments. Expected {num_args}".format(num_args=num_args))

    # corpus tools config(tools_config) is initialized with system and user config,
    # then some settings are overrided by config file specified thru command line option.
    tools_config = CorpusToolsConfig()
    if options.config is not None:
        tools_config.readfile(path.abspath(path.expanduser(options.config)))

    # clean tool depends on external tools/scripts, at least moses scripts.
    if len(tools_config.sections()) == 0:
        sys.stderr.write("Corpus tools config files not exist or broken. Please check the system and user config files.\n")
        sys.stderr.write("System: " + tools_config.SYSTEM_CONFIG + "\n")
        sys.stderr.write("User:   " + tools_config.USER_CONFIG + "\n")
        sys.exit(errno.EINVAL)

    steps_filename = args[4]
    clean_config = CleanConfig(path.abspath(path.expanduser(steps_filename)))
    if clean_config.validate_steps() is False:
        sys.stderr.write("Failed to read clean steps definition.\n")
        sys.exit(errno.EINVAL)

    clean_config.corpus_name = args[1]
    clean_config.source_lang = args[2]
    clean_config.target_lang = args[3]
    clean_config.infile_dir  = path.abspath(path.expanduser(args[0]))
    clean_config.outfile_dir = clean_config.infile_dir if options.output_dir is None \
                                else path.abspath(path.expanduser(options.output_dir))
    clean_config.working_dir = clean_config.infile_dir if options.working_dir is None \
                                else path.abspath(path.expanduser(options.working_dir))
    clean_config.log = path.abspath(path.expanduser(options.log)) if options.log is not None \
                                else path.join(clean_config.working_dir, '.'.join([clean_config.corpus_name, "clean", "log"]))

    if clean_config.validate_paths() is False:
        sys.exit(errno.ENOENT)

    return (tools_config, clean_config)


def clean_corpus(tools, clean):
    """
    Clean corpus files.

    Copy the corpus files into working directory, run the user-specified clean steps, keep the result for
    every steps, finally put the cleaned corpus files into output directory.

    Args
        :tools: configuration of external tools, e.g. tokenizers.
        :clean: clean configuration, include filenames, directories, source and target languages, clean steps, etc.

    Returns
        Quit the program if failed.
    """
    # prepare the corpus in working directory.
    if not path.samefile(clean.infile_dir, clean.working_dir):
        source_in = path.join(clean.infile_dir, '.'.join([clean.corpus_name, clean.source_lang]))
        target_in = path.join(clean.infile_dir, '.'.join([clean.corpus_name, clean.target_lang]))
        shutil.copy(source_in, clean.working_dir)
        shutil.copy(target_in, clean.working_dir)

    # backup the original corpus.
    source_corpus = clean.corpus_w(clean.source_lang)
    target_corpus = clean.corpus_w(clean.target_lang)
    shutil.copy(source_corpus, clean.corpus_w(clean.source_lang, 'orig'))
    shutil.copy(target_corpus, clean.corpus_w(clean.target_lang, 'orig'))

    # every clean step works on source_corpus and target_corpus ( corpus.{en,fr} ).
    # output corpus suffix with ext name, then copy output corpus into input corpus files for next steps.
    for step in clean.steps:
        module_name = "corpustools.clean." + step["name"]
        try:
            __import__(module_name)
            module = sys.modules[module_name]
            if 'predicate' in module.__dict__:
                predicate_clean(clean, step, module.predicate)
            else:
                module.run(clean, tools, step)
        except ImportError as e:
            print e
            sys.exit(errno.EPERM)

    # suffix the final output with ext name 'clean'.
    shutil.copy(source_corpus, clean.corpus_w(clean.source_lang, 'clean'))
    shutil.copy(target_corpus, clean.corpus_w(clean.target_lang, 'clean'))

    # copy the final cleaned corpus into output directory.
    if not path.samefile(clean.working_dir, clean.outfile_dir):
        shutil.copy(clean.corpus_w(clean.source_lang, 'clean'), clean.outfile_dir)
        shutil.copy(clean.corpus_w(clean.target_lang, 'clean'), clean.outfile_dir)


def predicate_clean(clean, step, predicate):
    """Clean the corpus files in a way called 'predicate clean'.

    Predicate clean can be applied to those clean rules which only accept or drop
    the align sentences from corpus according a predicate(a function return True or False).
    """
    ext = step["ext"]
    source_corpus = clean.corpus_w(clean.source_lang)
    target_corpus = clean.corpus_w(clean.target_lang)
    source_ext_corpus = clean.corpus_w(clean.source_lang, ext)
    target_ext_corpus = clean.corpus_w(clean.target_lang, ext)

    source_fp = codecs.open(source_corpus, 'r', encoding="utf-8")
    target_fp = codecs.open(target_corpus, 'r', encoding="utf-8")
    source_ext_fp = codecs.open(source_ext_corpus, 'w', encoding="utf-8")
    target_ext_fp = codecs.open(target_ext_corpus, 'w', encoding="utf-8")

    for source_line, target_line in zip(source_fp, target_fp):
        if predicate(source_line, target_line, step):
            source_ext_fp.write(source_line)
            target_ext_fp.write(target_line)

    source_ext_fp.close()
    target_ext_fp.close()
    source_fp.close()
    target_fp.close()
    shutil.copy(source_ext_corpus, source_corpus)
    shutil.copy(target_ext_corpus, target_corpus)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
