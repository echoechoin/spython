#ifndef _DECRYPY_SOURCE_FILE
#define _DECRIPT_SOURCE_FILE
#include <Python.h>
#include <math.h>

#include <openssl/aes.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

/**
 * @description: decrypt_file.c使用对称加密算法AES加密文件，密钥长度为128bit 
 * @dependencies: openssl
 */

#define KEY  "8cc72b05705d5c46f412af8cbed55aad"
#define IV   "667b02a85c61c786def4521b060265e8"
#define HEADINFO "encrypted-python-source-file-header"
#define _NO_DECRYPT_FILE_OUTPUT // 是否需要输出解密后的文件

// 可以使用的函数
int test(void);
FILE * d_open();

#endif