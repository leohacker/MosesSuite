#!/bin/bash

# Test moses installation.
# 
# Project:      Moses Suite
# URL:          http://github.com/leohacker/MosesSuite
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    2012, Leo Jiang
# License:      GPL

# set -x

# source the configuration to get the value of env MOSES_DATA_ROOT.
source /etc/moses-suite.conf

# Keep this directory consistent with definition in moses-suite-test.spec .
cd ${MOSES_DATA_ROOT}/translation_models/test/sample-models

echo "Test moses decoder"
echo "=================="
moses -f phrase-model/moses.ini < phrase-model/in > ~/out

read line < ~/out
if [ "$line" = "this is a small house" ]; then
    test_phrase="Passed"
else
    test_phrase="Failed"
fi

echo 
echo 
echo "Test moses chart decoder"
echo "========================"
moses_chart -f string-to-tree/moses.ini < string-to-tree/in > ~/out.stt
moses_chart -f tree-to-tree/moses.ini < tree-to-tree/in.xml > ~/out.ttt

read line < ~/out.stt
if [ "$line" = "this is a small house" ]; then
    test_string2tree="Passed"
else
    test_string2tree="Failed"
fi

read line < ~/out.ttt
if [ "$line" = "头顶上的 氧气 面罩 船舱 区 已滑落 。" ]; then
    test_tree2tree="Passed"
else
    test_tree2tree="Failed"
fi

rm ~/out
rm ~/out.stt
rm ~/out.ttt

echo
echo
echo "Test moses server xmlrpc"
echo "========================"
echo "launch moses server"
echo "-------------------"
mosesserver -f phrase-model/moses.ini --server-port 9090 &
pid_mosesserver=$!

# wait server launch completed.
sleep 10s

echo
echo
echo "run python xmlrpc client"
echo "------------------------"
moses-server-xmlrpc-test.py
ret=$?

echo ""
echo "kill the moses server process"
echo "-----------------------------"
kill -9 $pid_mosesserver

if [ $ret == 0 ]; then
    test_xmlrpc="Passed"
else
    test_xmlrpc="Failed"
fi

echo ""
echo "==========="
echo "Test Result"
echo "==========="
echo "[Moses] Phrase model: $test_phrase"
echo "[Moses chart] String2Tree: $test_string2tree"
echo "[Moses chart] Tree2Tree: $test_tree2tree"
echo "[Moses server] xmlrpc: $test_xmlrpc"
