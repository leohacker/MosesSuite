#!/bin/env python
# -*- coding: utf-8 -*-

# Simple test case for testing xmlrpc support in moses server which should 
# run with sample models.
#
# Project:      MosesSuite
# URL:          http://github.com/leohacker/MosesSuite
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    2012, Leo Jiang
# License:      GPL 
#
# Please launch the moses server with port 9090 first.

import sys
import xmlrpclib

try:
    proxy = xmlrpclib.ServerProxy("http://localhost:9090/RPC2")
    text_translate = proxy.translate({"text":"das ist ein kleines haus"})["text"]
    #text_translate = proxy.translate({"text":"This string from chinese"})["text"] 
except IOError as e:
    print e
    print "Please check whether moses server is launched sucessfully or on port 9090."
    sys.exit(2)

print ""
print "Translated text: +" + text_translate + "+" 
if text_translate == "this is a small house ":
    sys.exit(0)
else:
    print "Get the response from xmlrpc but translation is wrong."
    print "Please check whether launch the moses server with sample engine."
    sys.exit(1)
