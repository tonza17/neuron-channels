@echo off
REM Compile the de Rosenroll 2026 DSGC MOD files into nrnmech.dll using
REM NEURON's canonical Windows batch wrapper.
REM
REM Compiles the .mod files in ``sources/`` and emits ``nrnmech.dll`` back
REM into the same directory.
set "SCRIPT_DIR=%~dp0"
set "SOURCES_DIR=%SCRIPT_DIR%sources"
if not exist "%SOURCES_DIR%" (
    echo ERROR: sources directory not found at "%SOURCES_DIR%".
    exit /b 1
)
pushd "%SOURCES_DIR%"
call "C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat" "%SOURCES_DIR%"
set "RC=%ERRORLEVEL%"
popd
exit /b %RC%
