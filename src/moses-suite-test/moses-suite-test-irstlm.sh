#!/bin/bash

# Train a sample model with IRSTLM support for FR-EN. 
#
# Project:      Moses Suite
# URL:          http://github.com/leohacker/MosesSuite
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    Leo Jiang, 2012
# License:      GPL

set -x

# source common functions.
source moses-suite.functions
if [ $? != 0 ]; then
    echo "Failed to source moses-suite.functions."
    exit 1
fi

# source the moses configuration.
source_moses_conf

SCRIPTS_ROOT=${MOSES_SUITE_ROOT}/moses/scripts
check_dir "${SCRIPTS_ROOT}" "Moses script root directory."

TM_ROOT=${MOSES_DATA_ROOT}/translation_models/test/training-irstlm
check_dir "${TM_ROOT}"  "root directory of translation model training-irstlm"
if [ ! -w "${TM_ROOT}" ]; then
    echo "No permission for writing the directory ${TM_ROOT}"
    exit $E_ACCES
fi  
echo "Clean the directory: $TM_ROOT"
rm -rf ${TM_ROOT}/{model,lm,training,tuning,truecase-model,evaluation,corpus}

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

reuse_weights=${SCRIPTS_ROOT}/ems/support/reuse-weights.perl

check_file  "$train_model"      "script train-model "
check_file  "$moses"            "moses core"
check_dir   "$mertdir"          "mert directory"
check_file  "$mert_moses"       "script mert-moses"
check_file  "$processPhraseTable"   "processPhraseTable"
check_file  "$processLexicalTable"  "processLexicalTable"

check_file  "$reuse_weights"    "script reuse-weights"

filter_model_given_input=${SCRIPTS_ROOT}/training/filter-model-given-input.pl
check_file  "$filter_model_given_input" "script of filter model with given input"

multi_bleu=${SCRIPTS_ROOT}/generic/multi-bleu.perl
check_file "$multi_bleu" "script of bleu"

#train_recaser=${SCRIPTS_ROOT}/recaser/train-recaser.perl
#recaser=${SCRIPTS_ROOT}/recaser/recase.perl
#
#check_file  "$train_recaser"    "script train-recaser"
#check_file  "$recaser"          "script recaser"

# Prepare IRSTLM Corpus
# ============================================
cd ${TM_ROOT}
mkdir -p corpus/{lm,training,tuning,evaluation,truecaser}
mkdir {lm,training,tuning,evaluation,truecase-model}

# Extra step for test-irstlm.
# --------------------------
cp news-commentary-v7.fr-en.fr corpus/training/
cp news-commentary-v7.fr-en.en corpus/training/
cp news-test2008.fr corpus/tuning/
cp news-test2008.en corpus/tuning/
cp newstest2011.en corpus/evaluation/
cp newstest2011.fr corpus/evaluation/

# prepare training corpus.
# ------------------------
cd ${TM_ROOT}/corpus/training/
# tokenize the training corpus.
$tokenizer  -l en < news-commentary-v7.fr-en.en > news-commentary.tok.en
$tokenizer  -l fr < news-commentary-v7.fr-en.fr > news-commentary.tok.fr

# train the truecase model.
cd ${TM_ROOT}/truecase-model/
$train_truecaser --model truecase-model.en --corpus ${TM_ROOT}/corpus/training/news-commentary.tok.en
$train_truecaser --model truecase-model.fr --corpus ${TM_ROOT}/corpus/training/news-commentary.tok.fr

# truecase the training corpus.
cd ${TM_ROOT}/corpus/training/
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.fr < news-commentary.tok.fr > news-commentary.true.fr
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.en < news-commentary.tok.en > news-commentary.true.en

$clean_corpus_n news-commentary.true fr en news-commentary.clean 1 80

# prepare tuning corpus.
# ----------------------
cd ${TM_ROOT}/corpus/tuning
$tokenizer -l fr < news-test2008.fr > news-test2008.tok.fr
$tokenizer -l en < news-test2008.en > news-test2008.tok.en
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.fr < news-test2008.tok.fr > news-test2008.true.fr
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.en < news-test2008.tok.en > news-test2008.true.en

# prepare evaluation corpus.
# --------------------------
cd ${TM_ROOT}/corpus/evaluation
$tokenizer -l fr < newstest2011.fr > newstest2011.tok.fr
$tokenizer -l en < newstest2011.en > newstest2011.tok.en
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.fr < newstest2011.tok.fr > newstest2011.true.fr
$truecaser --model ${TM_ROOT}/truecase-model/truecase-model.en < newstest2011.tok.en > newstest2011.true.en

# Build Language Model and Train Phrase Model
# ===========================================
cd ${TM_ROOT}
# use irstlm to build lm.
$IRSTLM/bin/add-start-end.sh < corpus/training/news-commentary.true.en > lm/news-commentary.sb.en
cd lm
mkdir tmp
$IRSTLM/bin/build-lm.sh -i news-commentary.sb.en -t ./tmp -p -s improved-kneser-ney -o news-commentary.lm.en
$IRSTLM/bin/compile-lm --text yes news-commentary.lm.en.gz news-commentary.arpa.en

# binarise the output irstlm lm file using KenLM.
${MOSES_SUITE_ROOT}/moses/bin/build_binary news-commentary.arpa.en news-commentary.blm.en

echo "is this an English sentence ?" | ${MOSES_SUITE_ROOT}/moses/bin/query news-commentary.blm.en

# train phrase model
cd ${TM_ROOT}
${train_model} -scripts-root-dir ${SCRIPTS_ROOT} --root-dir ${TM_ROOT}/training --model-dir ${TM_ROOT}/model --corpus-dir ${TM_ROOT}/corpus/training/ --corpus ${TM_ROOT}/corpus/training/news-commentary.clean -f fr -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:${TM_ROOT}/lm/news-commentary.blm.en:8 >& ${TM_ROOT}/training/training.out

# Tuning 
# ======
${mert_moses} ${TM_ROOT}/corpus/tuning/news-test2008.true.fr ${TM_ROOT}/corpus/tuning/news-test2008.true.en $moses ${TM_ROOT}/model/moses.ini --working-dir ${TM_ROOT}/tuning/mert-work --mertdir $mertdir --rootdir ${SCRIPTS_ROOT} --decoder-flags="-threads 4 -v 0" &> ${TM_ROOT}/tuning/tuning.out 

mkdir bin-model
${processPhraseTable} -ttable 0 0 ${TM_ROOT}/model/phrase-table.gz -nscores 5 -out ${TM_ROOT}/bin-model/phrase-table
${processLexicalTable} -in ${TM_ROOT}/model/reordering-table.wbe-msd-bidirectional-fe.gz -out ${TM_ROOT}/bin-model/reordering-table
cp ${TM_ROOT}/tuning/mert-work/moses.ini ${TM_ROOT}/bin-model/moses.ini
cd bin-model
sed -i -e "/phrase-table/s|^0|1|" moses.ini
sed -i -e "s|model/phrase-table.gz|bin-model/phrase-table|" moses.ini
sed -i -e "s|model/reordering-table.wbe-msd-bidirectional-fe.gz|bin-model/reordering-table|" moses.ini

##${reuse_weights} ${TM_ROOT}/tuning/mert/moses.ini < ${TM_ROOT}/model/moses.ini > ${TM_ROOT}/tuning/moses-tuned.ini


# Evaluation
# ==========
# Filter Transaltion Model according to evaluation corpus
if [ -d ${TM_ROOT}/evaluation/filtered-newstest2011 ]; then
    rm -rf ${TM_ROOT}/evaluation/filtered-newstest2011
fi

$filter_model_given_input ${TM_ROOT}/evaluation/filtered-newstest2011 ${TM_ROOT}/tuning/mert-work/moses.ini ${TM_ROOT}/corpus/evaluation/newstest2011.true.fr -Binarizer ${processPhraseTable}

# Decoding Test Corpus
$moses -f ${TM_ROOT}/evaluation/filtered-newstest2011/moses.ini -input-file ${TM_ROOT}/corpus/evaluation/newstest2011.true.fr > ${TM_ROOT}/corpus/evaluation/newstest2011.translated.en 2> ${TM_ROOT}/evaluation/newstest2011.out

# Scoring
${multi_bleu} -lc ${TM_ROOT}/corpus/evaluation/newstest2011.true.en < ${TM_ROOT}/corpus/evaluation/newstest2011.translated.en
