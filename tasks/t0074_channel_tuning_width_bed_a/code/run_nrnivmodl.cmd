@echo off
REM Compile the t0074 MOD files into nrnmech.dll using the canonical NEURON wrapper.
REM Outputs nrnmech.dll into code/build/.
set "TASK_DIR=%~dp0"
set "MODDIR=%TASK_DIR%mods"
set "BUILDDIR=%TASK_DIR%build"
if not exist "%BUILDDIR%" mkdir "%BUILDDIR%"
pushd "%BUILDDIR%"
call "C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat" "%MODDIR%"
set "RC=%ERRORLEVEL%"
popd
exit /b %RC%
