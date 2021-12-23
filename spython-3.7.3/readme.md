# SPYTHON 3.7.3

## 一、修改Python源码（`仅针对Python-3.7.3`）

下载Python-3.7.3解释器的源码并对其进行如下的修改以运行加密的Python源码：
> 推荐使用[aliyun镜像](https://npm.taobao.org/mirrors/python/)下载python源码

### 1. 添加源文件

复制文件`path/to/spython/src/Python/decrypt_source_file.c` 到`path/to/spython/spython-3.7.3/Python-3.7.3/Python`中  
复制文件`path/to/spython/src/Include/decrypt_source_file.h`到`path/to/spython/spython-3.7.3/Python-3.7.3/Include`中

### 2. 添加解密函数到Python源码中

### 3. 禁止生成`.pyc`文件

### 4. 禁止访问字节码

由于开发者可以通过`.pyc`反编译出python源代码，所以需禁止生成`.pyc`文件

### 5. 修改`Makefile.pre.in`文件

### 6. 编译安装Python-3.7.3

```bash
tar path/to/spython/spython-3.7.3/Python-3.7.3.tgz
cd path/to/spython/spython-3.7.3/Python-3.7.3
# patch -p1 < ../enc.patch # 不想自己改就打我的补丁或者使用我改好的源码：Python-3.7.3-has-modified
./configure --prefix=$PREFIX
make
sudo make install

```

### 7. 编译安装spython-enc

```bash
cd path/to/spython
make
sudo make install
```
