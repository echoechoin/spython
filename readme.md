# SPYTHON

![alt](./src/demo.png)]

## 一、修改Python源码（`仅针对Python-2.7.15`）
下载Python-2.7.15解释器的源码并对其进行如下的修改以运行加密的Python源码：
> 推荐使用[aliyun镜像](https://npm.taobao.org/mirrors/python/)下载python源码

### 1. 添加文件
复制文件`./src/Python/decrypt_source_file.c`到`Python-2.7.15/Python`中  
复制文件`./src/Include/decrypt_source_file.h`到`Python-2.7.15/Python`中

### 2. 添加解密函数到Python源码中
```diff
diff --git a/Modules/main.c b/Modules/main.c
index a6edf82..3e69ca2 100644
--- a/Modules/main.c
+++ b/Modules/main.c
@@ -4,6 +4,7 @@
 #include "osdefs.h"
 #include "code.h" /* For CO_FUTURE_DIVISION */
 #include "import.h"
+#include "decrypt_source_file.h"
 
 #ifdef __VMS
 #include <unixlib.h>
@@ -607,7 +606,7 @@ Py_Main(int argc, char **argv)
         }
 
         if (sts==-1 && filename!=NULL) {
-            if ((fp = fopen(filename, "r")) == NULL) {
+            if ((fp = d_open(filename, "r")) == NULL) {
                 fprintf(stderr, "%s: can't open file '%s': [Errno %d] %s\n",
                     argv[0], filename, errno, strerror(errno));

diff --git a/Python/import.c b/Python/import.c
index 1d74faf..3a31846 100644
--- a/Python/import.c
+++ b/Python/import.c
@@ -14,6 +14,7 @@
 #include "eval.h"
 #include "osdefs.h"
 #include "importdl.h"
+#include "decrypt_source_file.h"
 
 #ifdef HAVE_FCNTL_H
 #include <fcntl.h>
@@ -1575,7 +1575,7 @@ find_module(char *fullname, char *subname, PyObject *path, char *buf,
             filemode = fdp->mode;
             if (filemode[0] == 'U')
                 filemode = "r" PY_STDIOTEXTMODE;
-            fp = fopen(buf, filemode);
+            fp = d_open(buf, filemode);
             if (fp != NULL) {
                 if (case_ok(buf, len, namelen, name))
                     break;

```

### 3. 禁止生成`.pyc`文件

由于开发者可以通过`.pyc`反编译出python源代码，所以需要禁用生成`.pyc`文件
```diff
--- a/Modules/main.c
+++ b/Modules/main.c
@@ -64,7 +64,6 @@ static char *usage_1 = "\
 Options and arguments (and corresponding environment variables):\n\
 -b     : issue warnings about comparing bytearray with unicode\n\
          (-bb: issue errors)\n\
--B     : don't write .py[co] files on import; also PYTHONDONTWRITEBYTECODE=x\n\
 -c cmd : program passed in as string (terminates option list)\n\
 -d     : debug output from parser; also PYTHONDEBUG=x\n\
 -E     : ignore PYTHON* environment variables (such as PYTHONPATH)\n\
@@ -375,9 +374,9 @@ Py_Main(int argc, char **argv)
             Py_OptimizeFlag++;
             break;
 
-        case 'B':
-            Py_DontWriteBytecodeFlag++;
-            break;
+        // case 'B':
+        //     Py_DontWriteBytecodeFlag++;
+        //     break;
 
         case 's':
             Py_NoUserSiteDirectory++;
@@ -443,7 +442,7 @@ Py_Main(int argc, char **argv)
 
         }
     }
-
+    Py_DontWriteBytecodeFlag++;
     if (help)
         return usage(0, argv[0]);
diff --git a/Python/pythonrun.c b/Python/pythonrun.c
index 44fe13d..c7a62ba 100644
--- a/Python/pythonrun.c
+++ b/Python/pythonrun.c
@@ -191,8 +191,8 @@ Py_InitializeEx(int install_sigs)
         Py_VerboseFlag = add_flag(Py_VerboseFlag, p);
     if ((p = Py_GETENV("PYTHONOPTIMIZE")) && *p != '\0')
         Py_OptimizeFlag = add_flag(Py_OptimizeFlag, p);
-    if ((p = Py_GETENV("PYTHONDONTWRITEBYTECODE")) && *p != '\0')
-        Py_DontWriteBytecodeFlag = add_flag(Py_DontWriteBytecodeFlag, p);
+    // if ((p = Py_GETENV("PYTHONDONTWRITEBYTECODE")) && *p != '\0')
+    //     Py_DontWriteBytecodeFlag = add_flag(Py_DontWriteBytecodeFlag, p);
     /* The variable is only tested for existence here; _PyRandom_Init will
        check its value further. */
     if ((p = Py_GETENV("PYTHONHASHSEED")) && *p != '\0')


```

### 4. 禁止访问字节码

```diff
diff --git a/Objects/codeobject.c b/Objects/codeobject.c
index a66aa69..33bc4eb 100644
--- a/Objects/codeobject.c
+++ b/Objects/codeobject.c
@@ -202,7 +202,7 @@ static PyMemberDef code_memberlist[] = {
     {"co_nlocals",      T_INT,          OFF(co_nlocals),        READONLY},
     {"co_stacksize",T_INT,              OFF(co_stacksize),      READONLY},
     {"co_flags",        T_INT,          OFF(co_flags),          READONLY},
-    {"co_code",         T_OBJECT,       OFF(co_code),           READONLY},
+    // {"co_code",         T_OBJECT,       OFF(co_code),           READONLY},
     {"co_consts",       T_OBJECT,       OFF(co_consts),         READONLY},
     {"co_names",        T_OBJECT,       OFF(co_names),          READONLY},
     {"co_varnames",     T_OBJECT,       OFF(co_varnames),       READONLY},
```

### 5. 修改`Makefile.pre.in`文件

Makefile需要链接`libssl`库，生成`decrypt_source_file.o`

```diff
diff --git a/Makefile.pre.in b/Makefile.pre.in
index 9297e7f..4e11afe 100644
--- a/Makefile.pre.in
+++ b/Makefile.pre.in
@@ -185,7 +185,7 @@ INSTSONAME=	@INSTSONAME@
 LIBS=		@LIBS@
 LIBM=		@LIBM@
 LIBC=		@LIBC@
-SYSLIBS=	$(LIBM) $(LIBC)
+SYSLIBS=	$(LIBM) $(LIBC)  -lcrypto -lssl
 SHLIBS=		@SHLIBS@
 
 THREADOBJ=	@THREADOBJ@
@@ -294,6 +294,7 @@ PGENOBJS=	$(POBJS) $(PGOBJS)
 
 ##########################################################################
 PYTHON_OBJS=	\
+		Python/decrypt_source_file.o \
 		Python/_warnings.o \
 		Python/Python-ast.o \
 		Python/asdl.o \
@@ -752,6 +753,7 @@ Python/formatter_string.o: $(srcdir)/Python/formatter_string.c \
 # Header files
 
 PYTHON_HEADERS= \
+		Include/decrypt_source_file.h \
 		Include/Python-ast.h \
 		Include/Python.h \
 		Include/abstract.h \

```

### 6. 编译安装Python-2.7.15

```
tar zxvf Python-2.7.15.tgz
cd Python-2.7.15
patch -p1 < ../enc.patch # 也可以自己修改，或者用我修改好的
./configure --prefix=$PREFIX
make
sudo make install

```

### 7. 编译安装spython-enc

修改目录到本仓库根目录

```bash
make
```

## 二、Contributor

[@echoechoin](https://github.com/echoechoin)   
> QQ: 614699596

## 三、Reference

[[1] 如何保护你的 Python 代码](https://zhuanlan.zhihu.com/p/54296517)  
[[2] Python 2.7.18 documentation](https://docs.python.org/2.7/)

have fun！🤣🤣🤣🤣🤣🤣
