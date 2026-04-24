@echo off
REM ----------------------------------------------------------------
REM Compile MOD files in code/sources/ into nrnmech.dll using NEURON's
REM Windows MinGW toolchain. Output: code/sources/x86_64/nrnmech.dll.
REM Idempotent: safe to re-run; nrnivmodl handles re-builds.
REM ----------------------------------------------------------------
set "MODDIR=%~dp0sources"
pushd "%MODDIR%"
call "C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat" .
set "RC=%ERRORLEVEL%"
popd
exit /b %RC%
