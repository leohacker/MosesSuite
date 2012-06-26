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
    echo "Corpus_Clean: Commandline Interface Testing"

    desc="Wrong arguments number"
    cmd='python corpus_clean.py dir filename en fr'
    run

    desc="Config file of clean steps"
    cmd='python corpus_clean.py dir filename en fr cleansteps'
    run

    desc="Paths validation - No option"
    cmd='python corpus_clean.py indir corpusname en fr test/cleansteps.conf'
    run

    desc="Paths validation - With options"
    cmd='python corpus_clean.py indir corpusname en fr test/cleansteps.conf -o outdir -w workingdir'
    run
}

echo "Corpus_Clean: Clean Steps Testing"
desc="clean steps"
cmd='python corpus_clean.py test corpus en fr test/cleansteps.conf -o test -w test -l test/clean.log'
run

rm -f test/clean.log
