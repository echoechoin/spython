@echo off
goto Run
:Usage
echo.%~nx0 [flags and arguments] [quoted MSBuild options]
echo.
echo.Build CPython from the command line.  Requires the appropriate
echo.version(s) of Microsoft Visual Studio to be installed (see readme.txt).
echo.
echo.After the flags recognized by this script, up to 9 arguments to be passed
echo.directly to MSBuild may be passed.  If the argument contains an '=', the
echo.entire argument must be quoted (e.g. `%~nx0 "/p:PlatformToolset=v100"`).
echo.Alternatively you can put extra flags for MSBuild in a file named 
echo.`msbuild.rsp` in the `PCbuild` directory, one flag per line. This file
echo.will be picked automatically by MSBuild. Flags put in this file does not
echo.need to be quoted. You can still use environment variables inside the 
echo.response file.
echo.
echo.Available flags:
echo.  -h  Display this help message
echo.  -r  Target Rebuild instead of Build
echo.  -d  Set the configuration to Debug
echo.  -e  Build external libraries fetched by get_externals.bat
echo.      Extension modules that depend on external libraries will not attempt
echo.      to build if this flag is not present
echo.  -m  Enable parallel build
echo.  -M  Disable parallel build (disabled by default)
echo.  -v  Increased output messages
echo.  -k  Attempt to kill any running Pythons before building (usually done
echo.      automatically by the pythoncore project)
echo.  --pgo          Build with Profile-Guided Optimization.  This flag
echo.                 overrides -c and -d
echo.
echo.Available flags to avoid building certain modules.
echo.These flags have no effect if '-e' is not given:
echo.  --no-ssl      Do not attempt to build _ssl
echo.  --no-tkinter  Do not attempt to build Tkinter
echo.  --no-bsddb    Do not attempt to build _bsddb
echo.
echo.Available arguments:
echo.  -c Release ^| Debug ^| PGInstrument ^| PGUpdate
echo.     Set the configuration (default: Release)
echo.  -p x64 ^| Win32
echo.     Set the platform (default: Win32)
echo.  -t Build ^| Rebuild ^| Clean ^| CleanAll
echo.     Set the target manually
echo.  --pgo-job  The job to use for PGO training; implies --pgo
echo.             (default: "-m test.regrtest --pgo")
exit /b 127

:Run
setlocal
set platf=Win32
set conf=Release
set target=Build
set dir=%~dp0
set parallel=
set verbose=/nologo /v:m
set kill=
set do_pgo=
set pgo_job=-m test.regrtest --pgo

:CheckOpts
if "%~1"=="-h" goto Usage
if "%~1"=="-c" (set conf=%2) & shift & shift & goto CheckOpts
if "%~1"=="-p" (set platf=%2) & shift & shift & goto CheckOpts
if "%~1"=="-r" (set target=Rebuild) & shift & goto CheckOpts
if "%~1"=="-t" (set target=%2) & shift & shift & goto CheckOpts
if "%~1"=="-d" (set conf=Debug) & shift & goto CheckOpts
if "%~1"=="-m" (set parallel=/m) & shift & goto CheckOpts
if "%~1"=="-M" (set parallel=) & shift & goto CheckOpts
if "%~1"=="-v" (set verbose=/v:n) & shift & goto CheckOpts
if "%~1"=="-k" (set kill=true) & shift & goto CheckOpts
if "%~1"=="--pgo" (set do_pgo=true) & shift & goto CheckOpts
if "%~1"=="--pgo-job" (set do_pgo=true) & (set pgo_job=%~2) & shift & shift & goto CheckOpts
rem These use the actual property names used by MSBuild.  We could just let
rem them in through the environment, but we specify them on the command line
rem anyway for visibility so set defaults after this
if "%~1"=="-e" (set IncludeExternals=true) & shift & goto CheckOpts
if "%~1"=="--no-ssl" (set IncludeSSL=false) & shift & goto CheckOpts
if "%~1"=="--no-tkinter" (set IncludeTkinter=false) & shift & goto CheckOpts
if "%~1"=="--no-bsddb" (set IncludeBsddb=false) & shift & goto CheckOpts

if "%IncludeExternals%"=="" set IncludeExternals=false
if "%IncludeSSL%"=="" set IncludeSSL=true
if "%IncludeTkinter%"=="" set IncludeTkinter=true
if "%IncludeBsddb%"=="" set IncludeBsddb=true

if "%IncludeExternals%"=="true" call "%dir%get_externals.bat"

if "%do_pgo%" EQU "true" if "%platf%" EQU "x64" (
    if "%PROCESSOR_ARCHITEW6432%" NEQ "AMD64" if "%PROCESSOR_ARCHITECTURE%" NEQ "AMD64" (
        echo.ERROR: Cannot cross-compile with PGO 
        echo.       32bit operating system detected. Ensure your PROCESSOR_ARCHITECTURE
        echo.       and PROCESSOR_ARCHITEW6432 environment variables are correct.
        exit /b 1 
    )
)

if "%GIT%" EQU "" set GIT=git
if exist "%GIT%" set GITProperty=/p:GIT="%GIT%"

rem Setup the environment
call "%dir%find_msbuild.bat" %MSBUILD%
if ERRORLEVEL 1 (call "%dir%env.bat" && set MSBUILD=msbuild)

if "%kill%"=="true" call :Kill

if "%do_pgo%"=="true" (
    set conf=PGInstrument
    call :Build %1 %2 %3 %4 %5 %6 %7 %8 %9
    del /s "%dir%\*.pgc"
    del /s "%dir%\..\Lib\*.pyc"
    echo on
    call "%dir%\..\python.bat" %pgo_job%
    @echo off
    call :Kill
    set conf=PGUpdate
    set target=Build
)
goto Build

:Kill
echo on
%MSBUILD% "%dir%\pythoncore.vcxproj" /t:KillPython %verbose%^
 /p:Configuration=%conf% /p:Platform=%platf%^
 /p:KillPython=true

@echo off
goto :eof

:Build
rem Call on MSBuild to do the work, echo the command.
rem Passing %1-9 is not the preferred option, but argument parsing in
rem batch is, shall we say, "lackluster"
echo on
%MSBUILD% "%dir%pcbuild.proj" /t:%target% %parallel% %verbose%^
 /p:Configuration=%conf% /p:Platform=%platf%^
 /p:IncludeExternals=%IncludeExternals%^
 /p:IncludeSSL=%IncludeSSL% /p:IncludeTkinter=%IncludeTkinter%^
 /p:IncludeBsddb=%IncludeBsddb% %GITProperty%^
 %1 %2 %3 %4 %5 %6 %7 %8 %9

@echo off
goto :eof
