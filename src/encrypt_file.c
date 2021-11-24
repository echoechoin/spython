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
 * @dependencies: libssl
 */

#define KEY  "8cc72b05705d5c46f412af8cbed55aad"
#define IV   "667b02a85c61c786def4521b060265e8"
#define _NO_DECRYPT_FILE_OUTPUT // 是否需要输出解密后的文件
#define HEADINFO "encrypted-python-source-file-header"

static unsigned char* str2hex (char *str);
static void encrypt_buf (char *raw_buf, char **encrpy_buf, int len);
static void decrypt_buf (char *raw_buf, char **encrpy_buf, int len);
int encrypt_file (char *src, char *dst);
int decrypt_open (char *filename);
int decrypt_file (char *src, char *dst);


/**
 * @description: 加密文件
 * @param src: 未加密源文件的名字
 * @param dst: 加密后文件的名字
 * @return 0表示成功加密, -1表示失败
 */
int encrypt_file (char *src, char *dst) {
    int src_fd = open (src, O_RDONLY);
    int dst_fd = open (dst, O_RDWR | O_CREAT);
    int size;
    char buf[64] ={0};
    char *en_buf = (char *) malloc (64);
    write(dst_fd, HEADINFO, sizeof(HEADINFO)-1);
    if (src_fd == -1)
        return -1;
    if (dst_fd == -1)
        return -1;
    while( (size = read (src_fd, buf, 64)) > 0) {
        encrypt_buf (buf, &en_buf, 64); 
        if (write (dst_fd, en_buf, 64) == -1)
            return -1;
        memset (buf, 0, 64);
        memset (en_buf, 0, 64);
    }
    free (en_buf);
    close (src_fd);
    close (dst_fd);
}

/**
 * @description: 打开加密文件，返回文件描述符
 * @param filename 表示需要解密的文件
 * @return 返回解密后的文件的文件描述符，失败返回-1
 */
int decrypt_open (char *filename)
{
    int ret = -1;
    int original_file_fd = open (filename, O_RDWR);
    int size = 0;
    char buf[64] = {0};
    char filehead[512] = {0};
    char *de_buf = (char *)malloc (64);

    char template[] = "decrypt-file-XXXXXX"; 
    ret = mkstemp (template);
    if (ret == -1){
        close(original_file_fd);
        return -1;
    }
        
    // 是否输出解密后的文件
#ifdef _NO_DECRYPT_FILE_OUTPUT
    unlink (template); 
#endif
    
    // 读取文件头
    size = read (original_file_fd, filehead, sizeof(HEADINFO)-1);
    if ( size < 0 ){
        close (original_file_fd);
        close (ret);
        return -1;
    }
    filehead[size] = 0;
    // 普通文件直接打开
    if(strcmp(filehead, HEADINFO) != 0) {
        close (ret);
        ret = original_file_fd;
        lseek (ret, 0, SEEK_SET);
        return ret;
    }

    // 加密文件解密后打开
    while ((size = read (original_file_fd, buf, 64)) > 0) {
        int end_pos = 0;
        decrypt_buf (buf, &de_buf, 64);
        for (int i = 63; i >= 0; i--) {
            if (de_buf[i] != 0) {
                end_pos = i + 1;
                break;
            }
        }
        if (write (ret, de_buf, end_pos) == -1) {
            close(original_file_fd);
            close(ret);
            return -1;
        }
        memset (buf,0,64);
    }
    lseek (ret,0,SEEK_SET);
    free (de_buf);
    close(original_file_fd);
    return ret;
}

unsigned char* str2hex (char *str) {
    unsigned char *ret = NULL;
    int str_len = strlen (str);
    int i = 0;
    assert ((str_len%2) == 0);
    ret = (char *) malloc (str_len/2);
    for (i =0;i < str_len; i = i + 2 ) {
        sscanf (str + i, "%2hhx", &ret[i / 2]);
    }
    return ret;
}

void encrypt_buf (char *raw_buf, char **encrpy_buf, int len) {
    AES_KEY aes;
    unsigned char *key = str2hex (KEY);
    unsigned char *iv  = str2hex (IV);
    AES_set_encrypt_key (key, 128, &aes);
    AES_cbc_encrypt (raw_buf, *encrpy_buf, len, &aes,iv, AES_ENCRYPT);
    free (key);
    free (iv);
}

void decrypt_buf (char *raw_buf, char **encrpy_buf, int len ) {
    AES_KEY aes;
    unsigned char *key = str2hex (KEY);
    unsigned char *iv  = str2hex (IV);
    AES_set_decrypt_key (key,128,&aes);
    AES_cbc_encrypt (raw_buf, *encrpy_buf, len, &aes, iv, AES_DECRYPT);
    free (key);
    free (iv);
}
