#!/bin/bash

# Train a model with IRSTLM support.
#
# Project:      Moses Suite
# URL:          http://github.com/leohacker/MosesSuite
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    Leo Jiang, 2012
# License:      GPL

# Usage:
#       moses-suite-irstlm-train src-lang tar-lang id

# May 16 2012   A simple script to train model with settings described same as moses core website.

export LC_ALL=C

# source common functions.
source moses-suite.functions
if [ $? != 0 ]; then
    echo "Failed to source moses-suite.functions."
    exit 1
fi

# check parameters number.
if [ $# != 3 ]; then
    echo "Usage: `basename $0` source_language target_language id"
    exit $E_INVAL
fi

src_lang=$1
tar_lang=$2
id=$3

# -- Normalize the src and target language ID. --
SRC=$( echo "$src_lang" | tr '[:lower:]' '[:upper:]' )
TARGET=$( echo "$tar_lang" | tr '[:lower:]' '[:upper:]' )

src=$( echo "$SRC" | tr '[:upper:]' '[:lower:]' )
target=$( echo "$TARGET" | tr '[:upper:]' '[:lower:]' )

# Copyleft declaration
version="1.0"
echo "Moses Suite Train Model -- Author: Leo Jiang <leo.jiang.dev@gmail.com>"
echo "Version: $version"
echo

set -x

# source the moses configuration.
source_moses_conf

SCRIPTS_ROOT=${MOSES_SUITE_ROOT}/moses/scripts
check_dir "${SCRIPTS_ROOT}" "Moses script root directory."

TM_ROOT=${MOSES_DATA_ROOT}/translation_models/${SRC}-${TARGET}/${id}
mkdir -p ${TM_ROOT}

check_dir "${TM_ROOT}"  "root directory of translation model"
if [ ! -w "${TM_ROOT}" ]; then
    echo "No permission for writing the directory ${TM_ROOT}"
    exit $E_ACCES
fi  
echo "Clean the directory: $TM_ROOT"
rm -rf ${TM_ROOT}/{bin-model,model,lm,training,tuning,truecase-model,evaluation,corpus}

CORPUS_ROOT=${MOSES_DATA_ROOT}/corpus/${SRC}-${TARGET}
check_dir "${CORPUS_ROOT}" "root directory of corpus in corpus repository."

IRSTLM=${MOSES_SUITE_ROOT}/irstlm
check_var IRSTLM
export IRSTLM

# Check the location of scritps and executable program.
# =====================================================
tokenizer=${SCRIPTS_ROOT}/tokenizer/tokenizer.perl
lowercaser=${SCRIPTS_ROOT}/tokenizer/lowercase.perl
detokenizer=${SCRIPTS_ROOT}/tokenizer/detokenizer.perl
clean_corpus_n=${SCRIPTS_ROOT}/training/clean-corpus-n.perl
train_truecaser=${SCRIPTS_ROOT}/recaser/train-truecaser.perl
truecaser=${SCRIPTS_ROOT}/recaser/truecase.perl

check_file "$tokenizer"     "European language tokenizer"
check_file "$lowercaser"    "lowercaser"
check_file "$detokenizer"   "detokenizer"
check_file "$clean_corpus_n"    "script clean long sentence"
check_file "$train_truecaser"   "script train truecase"
check_file "$truecaser"     "truecaser"

train_model=${SCRIPTS_ROOT}/training/train-model.perl
moses=${MOSES_SUITE_ROOT}/moses/bin/moses
mertdir=${MOSES_SUITE_ROOT}/moses/bin
mert_moses=${SCRIPTS_ROOT}/training/mert-moses.pl
processPhraseTable=${MOSES_SUITE_ROOT}/moses/bin/processPhraseTable
processLexicalTable=${MOSES_SUITE_ROOT}/moses/bin/processLexicalTable

check_file  "$train_model"      "script train-model "
check_file  "$moses"            "moses core"
check_dir   "$mertdir"          "mert directory"
check_file  "$mert_moses"       "script mert-moses"
check_file  "$processPhraseTable"   "processPhraseTable"
check_file  "$processLexicalTable"  "processLexicalTable"

filter_model_given_input=${SCRIPTS_ROOT}/training/filter-model-given-input.pl
check_file  "$filter_model_given_input" "script of filter model with given input"

multi_bleu=${SCRIPTS_ROOT}/generic/multi-bleu.perl
check_file "$multi_bleu" "script of bleu"

# Prepare IRSTLM Corpus
# ============================================
cd ${TM_ROOT}
mkdir -p corpus/{lm,training,tuning,evaluation,truecase}
mkdir {lm,training,tuning,evaluation,truecase-model}

# prepare training corpus.
# ------------------------
corpus_truecase=corpus_case
#corpus_lm=corpus_lm
corpus_training=corpus_training
corpus_tuning=corpus_tuning
corpus_eval=corpus_eval

cd ${TM_ROOT}/corpus/truecase/
check_file ${CORPUS_ROOT}/truecase/${corpus_truecase}.${src} "truecase corpus ${src}"
check_file ${CORPUS_ROOT}/truecase/${corpus_truecase}.${target} "truecase corpus ${target}"
cp ${CORPUS_ROOT}/truecase/${corpus_truecase}.${src} .
cp ${CORPUS_ROOT}/truecase/${corpus_truecase}.${target} .

# train truecase model.
cd ${TM_ROOT}/truecase-model/
$train_truecaser --model truecase-model.${src} --corpus ${TM_ROOT}/corpus/truecase/${corpus_truecase}.${src}
$train_truecaser --model truecase-model.${target} --corpus ${TM_ROOT}/corpus/truecase/${corpus_truecase}.${target}

#cd ${TM_ROOT}/corpus/lm/
#check_file ${CORPUS_ROOT}/lm/${corpus_lm}.${src} "lm corpus ${src}"
#check_file ${CORPUS_ROOT}/lm/${corpus_lm}.${target} "lm corpus ${target}"
#cp ${CORPUS_ROOT}/lm/${corpus_lm}.${src} .
#cp ${CORPUS_ROOT}/lm/${corpus_lm}.${target} .

cd ${TM_ROOT}/corpus/training/
check_file ${CORPUS_ROOT}/training/${corpus_training}.${src} "training corpus ${src}"
check_file ${CORPUS_ROOT}/training/${corpus_training}.${target} "training corps ${target}"
cp ${CORPUS_ROOT}/training/${corpus_training}.${src} corpus.tok.${src}
cp ${CORPUS_ROOT}/training/${corpus_training}.${target} corpus.tok.${target}

# truecase training corpus.
cd ${TM_ROOT}/corpus/training/
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${src} < corpus.tok.${src} > corpus.true.${src}
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${target} < corpus.tok.${target} > corpus.true.${target}

# Everything lowercased.  TODO: still right for truecase ?

# clean training corpus.

# One sentence per line, no empty lines.
# Sentences longer than 100 words (and their corresponding translations) 
# have to be eliminated (note that a shorter sentence length limit will speed up training.

# TODO: read the source code of clean_corpus_n
# clean_corpus_n perform the following steps:
# 1. removes empty lines
# 2. removes redundant space characters
# 3. drops lines (and their corresponding lines), that are empty, too short, 
# too long or violate the 9-1 sentence ratio limit of GIZA++ 
$clean_corpus_n corpus.true ${src} ${target} corpus.clean 1 80

# prepare tuning corpus.
# ----------------------
cd ${TM_ROOT}/corpus/tuning
check_file ${CORPUS_ROOT}/tuning/${corpus_tuning}.${src} "tuning corpus ${src}"
check_file ${CORPUS_ROOT}/tuning/${corpus_tuning}.${target} "tuning corps ${target}"

cp ${CORPUS_ROOT}/tuning/${corpus_tuning}.${src} corpus_tuning.tok.${src}
cp ${CORPUS_ROOT}/tuning/${corpus_tuning}.${target} corpus_tuning.tok.${target}
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${src} < corpus_tuning.tok.${src} > corpus_tuning.true.${src}
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${target} < corpus_tuning.tok.${target} > corpus_tuning.true.${target}

# prepare evaluation corpus.
# --------------------------
cd ${TM_ROOT}/corpus/evaluation
check_file ${CORPUS_ROOT}/evaluation/${corpus_eval}.${src} "eval corpus ${src}"
check_file ${CORPUS_ROOT}/evaluation/${corpus_eval}.${target} "eval corps ${target}"

cp ${CORPUS_ROOT}/evaluation/${corpus_eval}.${src} corpus_eval.tok.${src}
cp ${CORPUS_ROOT}/evaluation/${corpus_eval}.${target} corpus_eval.tok.${target}
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${src} < corpus_eval.tok.${src} > corpus_eval.true.${src}
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${target} < corpus_eval.tok.${target} > corpus_eval.true.${target}

# Build Language Model and Train Phrase Model
# ===========================================
cd ${TM_ROOT}
# use irstlm to build lm.
$IRSTLM/bin/add-start-end.sh < corpus/training/corpus.true.${target} > lm/corpus.sb.${target}
cd lm
mkdir tmp
$IRSTLM/bin/build-lm.sh -i corpus.sb.${target} -t ./tmp -p -s improved-kneser-ney -o corpus.lm.${target}
$IRSTLM/bin/compile-lm --text yes corpus.lm.${target}.gz corpus.arpa.${target}

# binarise the output irstlm lm file using KenLM.
${MOSES_SUITE_ROOT}/moses/bin/build_binary -i corpus.arpa.${target} corpus.blm.${target}

# train phrase model
# --parallel                parallel run some steps of nine steps if multiple processors.
# -mgiza -mgiza-cpus        using multi-threads version of giza++ and specify the number of CPU.
# --parts n                 training on large corpora.
# --parallel                run the two directions of GIZA++ as independent processes.

cd ${TM_ROOT}
${train_model} \
    --parallel \
    -mgiza -mgiza-cpus 4 \
    --scripts-root-dir ${SCRIPTS_ROOT} \
    --root-dir ${TM_ROOT}/training \
    --model-dir ${TM_ROOT}/model \
    --corpus-dir ${TM_ROOT}/corpus/training/ \
    --corpus ${TM_ROOT}/corpus/training/corpus.clean \
    --f ${src} --e ${target} \
    --alignment grow-diag-final-and \
    --reordering msd-bidirectional-fe \
    --lm 0:3:${TM_ROOT}/lm/corpus.blm.${target}:8 \
    &> ${TM_ROOT}/training/training.out

# Tuning 
# ======
${mert_moses} \
    ${TM_ROOT}/corpus/tuning/corpus_tuning.true.${src} \
    ${TM_ROOT}/corpus/tuning/corpus_tuning.true.${target} \
    $moses ${TM_ROOT}/model/moses.ini \
    --decoder-flags="-threads 4 -v 0" \
    --working-dir ${TM_ROOT}/tuning/mert-work \
    --mertdir $mertdir \
    --rootdir ${SCRIPTS_ROOT} \
    &> ${TM_ROOT}/tuning/tuning.out 

# Create binary model
# ===================
check_file "${TM_ROOT}/tuning/mert-work/moses.ini" "tuned moses config"

cd ${TM_ROOT}
mkdir bin-model
${processPhraseTable} -ttable 0 0 ${TM_ROOT}/model/phrase-table.gz -nscores 5 -out ${TM_ROOT}/bin-model/phrase-table
${processLexicalTable} -in ${TM_ROOT}/model/reordering-table.wbe-msd-bidirectional-fe.gz -out ${TM_ROOT}/bin-model/reordering-table

cp ${TM_ROOT}/tuning/mert-work/moses.ini ${TM_ROOT}/bin-model/moses.ini
#cp ${TM_ROOT}/model/moses.ini ${TM_ROOT}/bin-model/moses.ini
cd bin-model
sed -i -e "/phrase-table/s|^0|1|" moses.ini
sed -i -e "s|model/phrase-table.gz|bin-model/phrase-table|" moses.ini
sed -i -e "s|model/reordering-table.wbe-msd-bidirectional-fe.gz|bin-model/reordering-table|" moses.ini

# Evaluation
# ==========
## Filter Transaltion Model according to evaluation corpus
#if [ -d ${TM_ROOT}/evaluation/filtered-newstest2011 ]; then
#    rm -rf ${TM_ROOT}/evaluation/filtered-newstest2011
#fi
#
#$filter_model_given_input ${TM_ROOT}/evaluation/filtered-newstest2011 ${TM_ROOT}/tuning/mert-work/moses.ini ${TM_ROOT}/corpus/evaluation/newstest2011.true.fr -Binarizer ${processPhraseTable}
#
## Decoding Test Corpus
#$moses -f ${TM_ROOT}/evaluation/filtered-newstest2011/moses.ini -input-file ${TM_ROOT}/corpus/evaluation/newstest2011.true.fr > ${TM_ROOT}/corpus/evaluation/newstest2011.translated.en 2> ${TM_ROOT}/evaluation/newstest2011.out
#
## Scoring
#${multi_bleu} -lc ${TM_ROOT}/corpus/evaluation/newstest2011.true.en < ${TM_ROOT}/corpus/evaluation/newstest2011.translated.en
