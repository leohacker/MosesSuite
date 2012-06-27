#!/bin/bash

# Tune an IRSTLM model.
#
# Project:      Moses Suite
# URL:          http://github.com/leohacker/MosesSuite
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    Leo Jiang, 2012
# License:      GPL

# Usage:
#       moses-suite-irstlm-tune src-lang tar-lang engine-id

export LC_ALL=C

# source common functions.
source moses-suite.functions
if [ $? != 0 ]; then
    echo "Failed to source moses-suite.functions."
    exit 1
fi

# check parameters number.
if [ $# != 3 ]; then
    echo "Usage: `basename $0` source_lang target_lang id"
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
version="0.1"
echo "Moses Suite Tuning Script -- Author: Leo Jiang <leo.jiang.dev@gmail.com>"
echo "Version: $version"
echo

set -x

# source the moses configuration.
source_moses_conf

SCRIPTS_ROOT=${MOSES_SUITE_ROOT}/moses/scripts
check_dir "${SCRIPTS_ROOT}" "Moses script root directory."

TM_ROOT=${MOSES_DATA_ROOT}/translation_models/${SRC}-${TARGET}/${id}

check_dir "${TM_ROOT}"  "root directory of translation model"
if [ ! -w "${TM_ROOT}" ]; then
    echo "No permission for writing the directory ${TM_ROOT}"
    exit $E_ACCES
fi  

CORPUS_ROOT=${MOSES_DATA_ROOT}/corpus/${SRC}-${TARGET}
check_dir "${CORPUS_ROOT}" "root directory of corpus in corpus repository."

IRSTLM=${MOSES_SUITE_ROOT}/irstlm
check_var IRSTLM
export IRSTLM

train_model=${SCRIPTS_ROOT}/training/train-model.perl
moses=${MOSES_SUITE_ROOT}/moses/bin/moses
mertdir=${MOSES_SUITE_ROOT}/moses/bin
mert_moses=${SCRIPTS_ROOT}/training/mert-moses.pl
processPhraseTable=${MOSES_SUITE_ROOT}/moses/bin/processPhraseTable
processLexicalTable=${MOSES_SUITE_ROOT}/moses/bin/processLexicalTable

check_file  "$train_model"          "script train-model "
check_file  "$moses"                "moses core"
check_dir   "$mertdir"              "mert directory"
check_file  "$mert_moses"           "script mert-moses"
check_file  "$processPhraseTable"   "processPhraseTable"
check_file  "$processLexicalTable"  "processLexicalTable"

# prepare tuning corpus.
# ----------------------
cd ${TM_ROOT}
corpus_tuning=corpus_tuning
cd ${TM_ROOT}/corpus/tuning
check_file ${CORPUS_ROOT}/tuning/${corpus_tuning}.${src} "tuning corpus ${src}"
check_file ${CORPUS_ROOT}/tuning/${corpus_tuning}.${target} "tuning corps ${target}"

# we needn't to tokenize and truecase the corpus if already clean them with corpus_clean tool.
cp ${CORPUS_ROOT}/tuning/${corpus_tuning}.${src} corpus_tuning.true.${src}
cp ${CORPUS_ROOT}/tuning/${corpus_tuning}.${target} corpus_tuning.true.${target}
#cp ${CORPUS_ROOT}/tuning/${corpus_tuning}.${src} corpus_tuning.tok.${src}
#cp ${CORPUS_ROOT}/tuning/${corpus_tuning}.${target} corpus_tuning.tok.${target}
#$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${src} < corpus_tuning.tok.${src} > corpus_tuning.true.${src}
#$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${target} < corpus_tuning.tok.${target} > corpus_tuning.true.${target}

# Tuning 
# ======
cd ${TM_ROOT}
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
# verify whether the tuning step is successful.
check_file "${TM_ROOT}/tuning/mert-work/moses.ini" "tuned moses config"

cd ${TM_ROOT}
mkdir bin-model
${processPhraseTable} -ttable 0 0 ${TM_ROOT}/model/phrase-table.gz -nscores 5 -out ${TM_ROOT}/bin-model/phrase-table
${processLexicalTable} -in ${TM_ROOT}/model/reordering-table.wbe-msd-bidirectional-fe.gz -out ${TM_ROOT}/bin-model/reordering-table

cp ${TM_ROOT}/tuning/mert-work/moses.ini ${TM_ROOT}/bin-model/moses.ini
cd bin-model
sed -i -e "/phrase-table/s|^0|1|" moses.ini
sed -i -e "s|model/phrase-table.gz|bin-model/phrase-table|" moses.ini
sed -i -e "s|model/reordering-table.wbe-msd-bidirectional-fe.gz|bin-model/reordering-table|" moses.ini
