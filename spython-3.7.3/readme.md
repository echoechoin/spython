# SPYTHON 3.7.3

## 一、修改Python源码（`仅针对Python-3.7.3`）

下载Python-3.7.3解释器的源码并对其进行如下的修改以运行加密的Python源码：
> 推荐使用[aliyun镜像](https://npm.taobao.org/mirrors/python/)下载python源码

### 1. 添加源文件

复制文件`path/to/spython/src/Python/decrypt_source_file.c` 到`path/to/spython/spython-3.7.3/Python-3.7.3/Python`中  
复制文件`path/to/spython/src/Include/decrypt_source_file.h`到`path/to/spython/spython-3.7.3/Python-3.7.3/Include`中

### 2. 添加解密函数到Python源码中

```diff
diff --git a/Python/fileutils.c b/Python/fileutils.c
index 5e71d37..05b66fc 100644
--- a/Python/fileutils.c
+++ b/Python/fileutils.c
@@ -1,6 +1,7 @@
 #include "Python.h"
 #include "osdefs.h"
 #include <locale.h>
+#include "decrypt_source_file.h"
 
 #ifdef MS_WINDOWS
 #  include <malloc.h>
@@ -1252,7 +1253,7 @@ _Py_wfopen(const wchar_t *path, const wchar_t *mode)
     if (cpath == NULL) {
         return NULL;
     }
-    f = fopen(cpath, cmode);
+    f = d_open(cpath, cmode);
     PyMem_RawFree(cpath);
 #else
     f = _wfopen(path, mode);
diff --git a/fileio.c b/fileio.c
index 8bbe1ce..d9f2b0e 100644
--- a/fileio.c
+++ b/fileio.c
@@ -376,7 +376,7 @@ _io_FileIO___init___impl(fileio *self, PyObject *nameobj, const char *mode,
 #ifdef MS_WINDOWS
                 self->fd = _wopen(widename, flags, 0666);
 #else
-                self->fd = open(name, flags, 0666);
+                self->fd = dopen(name, flags, 0666);
 #endif
                 Py_END_ALLOW_THREADS
             } while (self->fd < 0 && errno == EINTR &&
```

### 3. 禁止生成`.pyc`文件

```diff
diff --git a/Modules/main.c b/Modules/main.c
index a745381..50e6043 100644
--- a/Modules/main.c
+++ b/Modules/main.c
@@ -85,7 +85,6 @@ static const char usage_1[] = "\
 Options and arguments (and corresponding environment variables):\n\
 -b     : issue warnings about str(bytes_instance), str(bytearray_instance)\n\
          and comparing bytes/bytearray with str. (-bb: issue errors)\n\
--B     : don't write .pyc files on import; also PYTHONDONTWRITEBYTECODE=x\n\
 -c cmd : program passed in as string (terminates option list)\n\
 -d     : debug output from parser; also PYTHONDEBUG=x\n\
 -E     : ignore PYTHON* environment variables (such as PYTHONPATH)\n\
@@ -817,9 +816,9 @@ pymain_parse_cmdline_impl(_PyMain *pymain, _PyCoreConfig *config,
             cmdline->optimization_level++;
             break;
 
-        case 'B':
-            cmdline->dont_write_bytecode++;
-            break;
+        // case 'B':
+        //     cmdline->dont_write_bytecode++;
+        //     break;
 
         case 's':
             cmdline->no_user_site_directory++;
@@ -891,6 +890,8 @@ pymain_parse_cmdline_impl(_PyMain *pymain, _PyCoreConfig *config,
             return 1;
         }
     } while (1);
+    
+    cmdline->dont_write_bytecode++;
 
     if (pymain->command == NULL && pymain->module == NULL
         && _PyOS_optind < pymain->argc
```

### 4. 禁止访问字节码

由于开发者可以通过`.pyc`反编译出python源代码，所以需禁止生成`.pyc`文件

```diff
diff --git a/Objects/codeobject.c b/Objects/codeobject.c
index 7ef0125..23ea5d4 100644
--- a/Objects/codeobject.c
+++ b/Objects/codeobject.c
@@ -277,7 +277,7 @@ static PyMemberDef code_memberlist[] = {
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

```diff
diff --git a/Makefile.pre.in b/Makefile.pre.in
index 2d2e11f..01de091 100644
--- a/Makefile.pre.in
+++ b/Makefile.pre.in
@@ -230,7 +230,7 @@ INSTSONAME=	@INSTSONAME@
 LIBS=		@LIBS@
 LIBM=		@LIBM@
 LIBC=		@LIBC@
-SYSLIBS=	$(LIBM) $(LIBC)
+SYSLIBS=	$(LIBM) $(LIBC) -lssl -lcrypto
 SHLIBS=		@SHLIBS@
 
 DLINCLDIR=	@DLINCLDIR@
@@ -329,6 +329,7 @@ PGENOBJS=	$(POBJS) $(PGOBJS)
 # Python
 
 PYTHON_OBJS=	\
+		Python/decrypt_source_file.o \
 		Python/_warnings.o \
 		Python/Python-ast.o \
 		Python/asdl.o \
```

### 6. 编译安装Python-3.7.3

```bash
tar path/to/spython/spython-3.7.3/Python-3.7.3.tgz
cd path/to/spython/spython-3.7.3/Python-3.7.3
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
