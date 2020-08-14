#!/bin/python2.7
#coding=utf-8
try:
    from progress_webray.bar import Bar
except:
    from src.progress_webray.bar import Bar
import os, sys, json
from optparse import OptionParser
from ctypes import *


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


# optparser
Usage = "\n  %s -h, --help   show this help message and exit\n\
  %s <configure file> Specify configure file." % (sys.argv[0], sys.argv[0])
parser = OptionParser(usage=Usage)
(options, args) = parser.parse_args()
args = eval(str(args))
if len(args) < 1:
    print ("warning: need to specify configure file.\n")
    exit(-1)
if len(args) > 1:
    print ("warning: unexpected configure file:"),
    for arg in args:
        print('"' + arg+ '"' + ','),
    exit(-1)
print("")

# 全局变量
bar = Bar('processing...', max=50)
bar.color = "green"

libdecfile = None

enc_file_list = []
except_file_list = []

conf_file_name = args[0]
conf_fp = open(conf_file_name)
try:
    conf_dict = byteify(json.loads(conf_fp.read()))
except:
    print("error: parse configure file failed!")
    exit(-1)
# 检查配置文件中的option`类型`是否正确，判断配置文件里有没有select和archive选项、是否为绝对路径。 except选项是可选选项

if not "archive" in conf_dict:
    print("error: no \"arcvive\" option. please specify where save encripted directory.\n")
    exit(-1)

if not isinstance(conf_dict["select"], str):
    print("error: unexpected type of \"select\" option. string need.\n")
    exit(-1)

if not isinstance(conf_dict["archive"], str):
    print("error: unexpected type of \"archive\" option. string need.\n")
    exit(-1)

if "except" in conf_dict:
    if not isinstance(conf_dict["except"], list):
        print("error: unexpected type of \"except\" option. list need.\n")
        exit(-1)
    else:
        for i in conf_dict["except"]:
            if not isinstance(i, str):
                print("error: unexpected type of \"except\": '%s'. string need.\n"%i)
                exit(-1)
            if list(i)[0] == '/':
                print("error: '%s' is not a relative path.\n"%i)
                exit(-1)
            except_file_list.append(i)

select_dir = conf_dict["select"]
archive_dir = conf_dict["archive"]

if list(select_dir)[0] != '/':
    print list(select_dir)[0]
    print("error: '%s' is not a absolute path.\n"%select_dir)
    exit(-1)

if list(archive_dir)[0] != '/':
    print("error: '%s' is not a absolute path.\n"%archive_dir)
    exit(-1)

# 创建加密后的文件夹 configure.json "archive"
if not os.path.isdir(select_dir):
    print("error: '%s' is not a directory.\n")
    exit(-1)

if select_dir == archive_dir:
    print("error: select directory and archive file can not be same file.\n")
    exit(-1)
if os.path.exists(archive_dir):
    f = raw_input("warning: archive file \"%s\" is exists, Do you want to override the file? (yes or no): " % archive_dir)
    while True:
        if f == "yes":
            os.system("rm  %s -rf"%archive_dir)
            break
        elif f == "no":
            exit(-1)
        else:
            raw_input ("yes or no: ")
os.system("cp %s %s -r"%(select_dir, archive_dir))




# 添加需要加密的文件 configure.json 使用绝对路径
def select_file(filename, enc_file_list):
    info = ""
    if os.path.splitext(filename)[-1] == ".pyc":
        info = " deleted"
    elif os.path.splitext(filename)[-1] != ".py":
        info = " passed"
    #print ("read: %s" % filename + info)
    enc_file_list.append(filename)


# 移除不需要解密的文件 configure.json 使用绝对路径 `时间复杂度O(n^2)`
def except_file(filename, enc_file_list):
    for f in enc_file_list:
        if os.path.samefile(filename, f):
            enc_file_list.remove(f)

print ("reading from 'select' option...  ")
def file_process(filename, handle):
    """
    对于`path`中的每一个文件，都调用handle(filename)进行处理
    """
    if os.path.isfile(filename) and not os.path.islink(filename):
        handle(filename, enc_file_list)
    elif os.path.isdir(filename) and not os.path.islink(filename):
        files = [os.path.realpath(filename + '/' + f) for f in os.listdir(filename)]
        for f in files:
            file_process(f, handle)
    else:
        print("waring: unexpected file: %s. <passed> "%filename)
print ("read finish.")

# 获取动态库对象
libdecfile = CDLL("libdecfile.so")

# 选择文件
file_process(archive_dir, select_file)

# 排除文件
for f in except_file_list:
    file_process(archive_dir + '/' + f, except_file)


# 开始加密
bar.max = len(enc_file_list)
for index, f in enumerate(enc_file_list):
    # 删除.pyc
    if os.path.splitext(f)[-1] == ".pyc":
        os.remove(f)
    # 加密.py
    elif os.path.splitext(f)[-1] == ".py":
        libdecfile.encrypt_file(f, f + "tmp")
        os.remove(f)
        os.rename(f + "tmp", f)
    # 其他类型的文件处理
    else:
        pass
    bar.next()
bar.finish()
print("success!\n")
exit(0)

