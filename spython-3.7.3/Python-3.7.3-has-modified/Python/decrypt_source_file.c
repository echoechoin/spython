#include "decrypt_source_file.h"

static unsigned char* str2hex (char *str);
static void encrypt_buf (char *raw_buf, char **encrpy_buf, int len);
static void decrypt_buf (char *raw_buf, char **encrpy_buf, int len);
static int decrypt_open (char *filename);


/**
 * @description 用于替换源码中的fopen(file, "r"); 
 */
FILE* d_open(char *filename, const char *modes)
{
    if (strcmp(modes, "r") != 0) {
        return fopen(filename, modes);
    }
    FILE *ret = NULL;
    int fd;
    fd = decrypt_open(filename);
    if ( fd < 0 ){
       // perror("error");
        return ret;
    }
    ret = fdopen(fd, modes);

    return ret;
}

/**
 * @description 用于替换源码中的open(pathname, flags, mode) 
 */
int dopen(const char *pathname, int flags, mode_t mode)
{
#ifdef O_CLOEXEC
    if (flags != (O_RDONLY | O_CLOEXEC))
#else
    if (flags != O_RDONLY)
#endif
        return open(pathname, flags, mode);
    else
        return decrypt_open(pathname);
}

/**
 * @description: 打开加密文件，返回文件描述符
 * @param filename 表示需要解密的文件
 * @return 返回解密后的文件的文件描述符，失败返回-1
 */
static int decrypt_open (char *filename)
{
    int ret = -1;
    int original_file_fd = open (filename, O_RDONLY);
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

static unsigned char* str2hex (char *str) {
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

static void decrypt_buf (char *raw_buf, char **encrpy_buf, int len ) {
    AES_KEY aes;
    unsigned char *key = str2hex (KEY);
    unsigned char *iv  = str2hex (IV);
    AES_set_decrypt_key (key,128,&aes);
    AES_cbc_encrypt (raw_buf, *encrpy_buf, len, &aes, iv, AES_DECRYPT);
    free (key);
    free (iv);
}
