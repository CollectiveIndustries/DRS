title Computer Warehouse Infection Removal Launcher
@echo off
color 27
cls
c:
cd \

@echo .
@echo ***** Launching Malwarebytes Antimalware Installer (MBAM) *****
@echo . 
start \\nas\tech\Infection Removal\Malwarebytes.exe

@echo .
@echo ***** Launching Spybot *****
@echo .
start \\nas\tech\Infection Removal\SpybotPortable\SpybotPortable.exe

@echo .
@echo ***** Launching Super Anti-Spyware (SAS) *****
@echo .


IF %PROCESSOR_ARCHITECTURE% == x86 (IF NOT DEFINED PROCESSOR_ARCHITEW6432 goto bit32)
goto bit64

:bit32
echo 32-bit SAS
start \\nas\tech\Infection Removal\SUPERAntiSpyware x86\SUPERANTISPYWARE.exe
goto cont

:bit64
echo 64-bit SAS
start \\nas\tech\Infection Removal\SUPERAntiSpyware x64\SUPERANTISPYWARE.exe

:cont

@echo .
@echo ***** Launching Emisoft Emergancy Kit Scanner (A2) *****
@echo .
start \\nas\tech\Infection Removal\Emsisoft Emergency Kit A2\Start Emergency Kit Scanner.exe
