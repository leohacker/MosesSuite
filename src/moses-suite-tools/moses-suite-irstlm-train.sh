#!/bin/bash

# Train an IRSTLM model.
#
# Project:      Moses Suite
# URL:          http://github.com/leohacker/MosesSuite
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    Leo Jiang, 2012
# License:      GPL

# Usage:
#       moses-suite-irstlm-train src-lang tar-lang id

export LC_ALL=C

# source common functions.
source moses-suite.functions
if [ $? != 0 ]; then
    echo "Failed to source moses-suite.functions."
    exit 1
fi

# check parameters number.
if [ $# != 3 ]; then
    echo "Usage: `basename $0` source_lang target_lang engine_id"
    exit $E_INVAL
fi

src_lang=$1
tgt_lang=$2
id=$3

# -- Normalize the src and target language ID. --
SRC=$( echo "$src_lang" | tr '[:lower:]' '[:upper:]' )
TGT=$( echo "$tgt_lang" | tr '[:lower:]' '[:upper:]' )

src=$( echo "$SRC" | tr '[:upper:]' '[:lower:]' )
tgt=$( echo "$TGT" | tr '[:upper:]' '[:lower:]' )

# Copyleft declaration
version="0.2"
echo "Moses Suite Training Script -- Author: Leo Jiang <leo.jiang.dev@gmail.com>"
echo "Version: $version"
echo

set -x

# source the moses configuration.
source_moses_conf

SCRIPTS_ROOT=${MOSES_SUITE_ROOT}/moses/scripts
check_dir "${SCRIPTS_ROOT}" "Moses script root directory."

TM_ROOT=${MOSES_DATA_ROOT}/translation_models/${SRC}-${TGT}/${id}
if [ -d "${TM_ROOT}" ]; then
    rm -rf ${TM_ROOT}
fi
mkdir -p ${TM_ROOT}

check_dir "${TM_ROOT}"  "root directory of translation model"
if [ ! -w "${TM_ROOT}" ]; then
    echo "No permission for writing the directory ${TM_ROOT}"
    exit $E_ACCES
fi  

CORPUS_ROOT=${MOSES_DATA_ROOT}/corpus/${SRC}-${TGT}
check_dir "${CORPUS_ROOT}" "root directory of corpus in corpus repository."

IRSTLM=${MOSES_SUITE_ROOT}/irstlm
check_var IRSTLM
export IRSTLM

# Check the location of scritps and executable program.
# =====================================================
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

# Prepare IRSTLM Corpus
# ============================================
cd ${TM_ROOT}
mkdir -p corpus/{lm,training,truecase}
mkdir {lm,training,truecase-model}

# prepare training corpus.
# ------------------------
#corpus_truecase=corpus_case
#corpus_lm=corpus_lm
corpus_training=corpus_training

#cd ${TM_ROOT}/corpus/truecase/
#check_file ${CORPUS_ROOT}/truecase/${corpus_truecase}.${src} "truecase corpus ${src}"
#check_file ${CORPUS_ROOT}/truecase/${corpus_truecase}.${tgt} "truecase corpus ${tgt}"
#cp ${CORPUS_ROOT}/truecase/${corpus_truecase}.${src} .
#cp ${CORPUS_ROOT}/truecase/${corpus_truecase}.${tgt} .
#
## train truecase model.
#cd ${TM_ROOT}/truecase-model/
#$train_truecaser --model truecase-model.${src} --corpus ${TM_ROOT}/corpus/truecase/${corpus_truecase}.${src}
#$train_truecaser --model truecase-model.${tgt} --corpus ${TM_ROOT}/corpus/truecase/${corpus_truecase}.${tgt}

#cd ${TM_ROOT}/corpus/lm/
#check_file ${CORPUS_ROOT}/lm/${corpus_lm}.${src} "lm corpus ${src}"
#check_file ${CORPUS_ROOT}/lm/${corpus_lm}.${tgt} "lm corpus ${tgt}"
#cp ${CORPUS_ROOT}/lm/${corpus_lm}.${src} .
#cp ${CORPUS_ROOT}/lm/${corpus_lm}.${tgt} .

cd ${TM_ROOT}/corpus/training/
check_file ${CORPUS_ROOT}/training/${corpus_training}.${src} "training corpus ${src}"
check_file ${CORPUS_ROOT}/training/${corpus_training}.${tgt} "training corps ${tgt}"
cp ${CORPUS_ROOT}/training/${corpus_training}.${src} corpus.tok.${src}
cp ${CORPUS_ROOT}/training/${corpus_training}.${tgt} corpus.tok.${tgt}

## truecase training corpus.
#cd ${TM_ROOT}/corpus/training/
#$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${src} < corpus.tok.${src} > corpus.true.${src}
#$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.${tgt} < corpus.tok.${tgt} > corpus.true.${tgt}
cp corpus.tok.${src} corpus.true.${src}
cp corpus.tok.${tgt} corpus.true.${tgt}
cp corpus.true.${src} corpus.clean.${src}
cp corpus.true.${tgt} corpus.clean.${tgt}

# Everything lowercased.  TODO: still right for truecase ?

# Build Language Model and Train Phrase Model
# ===========================================
cd ${TM_ROOT}
# use irstlm to build lm.
$IRSTLM/bin/add-start-end.sh < corpus/training/corpus.true.${tgt} > lm/corpus.sb.${tgt}
cd lm
mkdir tmp
$IRSTLM/bin/build-lm.sh -i corpus.sb.${tgt} -t ./tmp -p -s improved-kneser-ney -o corpus.lm.${tgt}
$IRSTLM/bin/compile-lm --text yes corpus.lm.${tgt}.gz corpus.arpa.${tgt}

# binarise the output irstlm lm file using KenLM.
${MOSES_SUITE_ROOT}/moses/bin/build_binary -i corpus.arpa.${tgt} corpus.blm.${tgt}

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
    --f ${src} --e ${tgt} \
    --alignment grow-diag-final-and \
    --reordering msd-bidirectional-fe \
    --lm 0:3:${TM_ROOT}/lm/corpus.blm.${target}:8 \
    &> ${TM_ROOT}/training/training.out

# Create binary model
# ===================
cd ${TM_ROOT}
mkdir bin-model
${processPhraseTable} -ttable 0 0 ${TM_ROOT}/model/phrase-table.gz -nscores 5 -out ${TM_ROOT}/bin-model/phrase-table
${processLexicalTable} -in ${TM_ROOT}/model/reordering-table.wbe-msd-bidirectional-fe.gz -out ${TM_ROOT}/bin-model/reordering-table

cp ${TM_ROOT}/model/moses.ini ${TM_ROOT}/bin-model/moses.ini
cd bin-model
sed -i -e "/phrase-table/s|^0|1|" moses.ini
sed -i -e "s|model/phrase-table.gz|bin-model/phrase-table|" moses.ini
sed -i -e "s|model/reordering-table.wbe-msd-bidirectional-fe.gz|bin-model/reordering-table|" moses.ini
