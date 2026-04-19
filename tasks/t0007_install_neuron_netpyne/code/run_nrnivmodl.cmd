@echo off
REM Run nrnivmodl on the task's mod directory.
REM Wall-clock-friendly: single cmd.exe entry that calls NEURON's own .bat wrapper.
set "MODDIR=%~dp0..\data\mod"
call "C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat" "%MODDIR%"
exit /b %ERRORLEVEL%
