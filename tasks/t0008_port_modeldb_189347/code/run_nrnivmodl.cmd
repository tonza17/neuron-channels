@echo off
REM Run nrnivmodl on a specified MOD directory from a specified build directory.
REM Arguments:
REM   %1 = MOD source directory (absolute path)
REM   %2 = build directory (absolute path; nrnmech.dll is emitted here)
REM Uses NEURON's canonical Windows batch wrapper.
set "MODDIR=%~1"
set "BUILDDIR=%~2"
if "%MODDIR%"=="" (
    echo ERROR: MOD source directory is required as arg 1.
    exit /b 1
)
if "%BUILDDIR%"=="" (
    echo ERROR: build directory is required as arg 2.
    exit /b 1
)
if not exist "%BUILDDIR%" mkdir "%BUILDDIR%"
pushd "%BUILDDIR%"
call "C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat" "%MODDIR%"
set "RC=%ERRORLEVEL%"
popd
exit /b %RC%
