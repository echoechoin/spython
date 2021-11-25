#!/bin/python2
# coding=utf-8
from ctypes import *
import sys
import os

if len(sys.argv) == 3:
    need_to_enc_file_name, after_enc_file_name = sys.argv[1:3]
    if not os.path.isfile(need_to_enc_file_name):
        print ("%s is not a file"%need_to_enc_file_name)
else:
    print ("need 2 args: %s <need_to_enc_file_name> <after_enc_file_name>"%sys.argv[0])
    exit(-1)

try:
    libdecfile = CDLL("./libencfile.so")
except:
    libdecfile = CDLL("libencfile.so")
libdecfile.encrypt_file(need_to_enc_file_name, after_enc_file_name)
os.system("chmod 0755 %s"%after_enc_file_name)
