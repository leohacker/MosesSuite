#!/bin/bash

function run() {
    echo "================================================================================"
    number=`expr $number + 1`
    echo "TestCase $number: $desc"
    echo $cmd 
    $cmd
    echo
}

cd ..
export PYTHONPATH=`pwd`
number=0

function test_cmdline_interface() {
    echo "clean-corpus: Commandline Interface Testing"

    desc="Wrong arguments number"
    cmd='python clean-corpus.py dir filename en fr'
    run

    desc="Config file of clean steps"
    cmd='python clean-corpus.py dir filename en fr cleansteps'
    run

    desc="Paths validation - No option"
    cmd='python clean-corpus.py indir corpusname en fr test/cleansteps.conf'
    run

    desc="Paths validation - With options"
    cmd='python clean-corpus.py indir corpusname en fr test/cleansteps.conf -o outdir -w workingdir'
    run
}

echo "clean-corpus: Clean Steps Testing"
cp test/corpus.orig.en test/corpus.en
cp test/corpus.orig.fr test/corpus.fr
desc="clean steps"
cmd='python clean-corpus.py test corpus en fr test/cleansteps.conf -o test -w test -l test/clean.log'
run

rm -f test/clean.log
