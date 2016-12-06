title Computer Warehouse Scanning Prep Tool
@echo off
color 27
cls
c:
cd \

@echo.
@echo ********** Disabling hibernation, sleep mode, and screensaver **********
@echo.
reg add "HKCU\Control Panel\Desktop" /v ScreenSaveActive /t REG_SZ /d 0 /f
reg delete "HKCU\Control Panel\Desktop" /v SCRNSAVE.EXE /f >nul 2>&1
powercfg -h off
powercfg -change -monitor-timeout-ac 0
powercfg -change -disk-timeout-ac 0
powercfg -change -standby-timeout-ac 0
powercfg -change -hibernate-timeout-ac 0

@echo.
@echo ********** Removing restore points and recycle bin**********
@echo.
vssadmin resize shadowstorage /For=C: /On=C: /MaxSize=1GB
rd /s /q %systemdrive%\$Recycle.bin

@echo.
@echo ********** Disabling automatic reboot for Microsoft updates **********
@echo.
reg add HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU /v NoAutoRebootWithLoggedOnUsers /t REG_DWORD /d 00000001 /f

@echo.
@echo ********** Resetting internet options **********
@echo. 
reg add HKCU\SOFTWARE\Microsoft\Windows\ /v ProxyEnable /t REG_DWORD /d 00000000 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
rundll32 inetcpl.cpl ResetIEtoDefaults
rem reg add "HKCU\Software\Microsoft\Internet Explorer\Main" /v "Search Page" /d http://www.google.com /f
rem reg add "HKCU\Software\Microsoft\Internet Explorer\Main" /v "Search Bar" /d http://www.google.com/ie /f
rem reg add "HKLM\Software\Microsoft\Internet Explorer\Search" /v "SearchAssistant" /d http://www.google.com/ie /f

@echo.
@echo ********** Resetting Chrome Browser settings **********
@echo.
if exist "%userprofile%\AppData\Local\Google\Chrome\Application\chrome.exe" cd "%userprofile%\AppData\Local\Google\Chrome\Application\"
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" cd C:\Program Files\Google\Chrome\Application"
if exist "c:\Program Files (x86)\Google\Chrome\Application\chrome.exe" cd "c:\Program Files (x86)\Google\Chrome\Application"
if exist chrome.exe start chrome "chrome://settings/resetProfileSettings"
if exist chrome.exe @echo Chrome Browser has been reset
if not exist chrome.exe @echo Chrome Browser not installed

@echo.
@echo ********** Resetting Firefox Browser settings **********
@echo.
if exist "C:\Program Files\Mozilla Firefox\firefox.exe" cd if exist "C:\Program Files\Mozilla Firefox"
if exist "C:\Program Files (x86)\Mozilla Firefox" cd "C:\Program Files (x86)\Mozilla Firefox"
if exist firefox.exe start firefox "about:support"
if exist firefox.exe @echo Firefox Browser has been reset
if not exist firefox.exe @echo Firefox Browser not installed
@echo.
pause
if exist "%userprofile%\desktop\Old Firefox Data" rmdir "%userprofile%\desktop\Old Firefox Data" /s /q

@echo.
@echo ********** Resetting registry keys for Google Chrome updates **********
@echo.
reg add HKLM\SOFTWARE\Policies\Google\Update /v UpdateDefault /t REG_DWORD /d 00000001 /f >nul 2>&1
reg add HKLM\SOFTWARE\Policies\Google\Update /v AutoUpdateCheckPeriodMinutes /t REG_DWORD /d 00000000 /f >nul 2>&1
reg add HKLM\SOFTWARE\Policies\Google\Update /v DisableAutoUpdateChecksCheckboxValue /t REG_DWORD /d 00000001 /f >nul 2>&1
reg add HKLM\SOFTWARE\Policies\Google\Update /v Update{8A69D345-D564-463C-AFF1-A69D9E530F96} /t REG_DWORD /d 00000000 /f >nul 2>&1

@echo.
@echo **********  Removing HitmanPro ********** 
@echo.
rmdir c:\ProgramData\HitmanPro /s /q >nul 2>&1
reg delete HKLM\Software\HitmanPro /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Minimal\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Minimal\hitmanpro36.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Minimal\hitmanpro36Crusader /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Minimal\hitmanpro36CrusaderBoot /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Minimal\hitmanpro37 /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Minimal\hitmanpro37.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro36.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro36Crusader /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro36CrusaderBoot /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro37 /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro37.sys /f >nul 2>&1

reg delete HKLM\System\ControlSet002\Control\SafeBoot\Minimal\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Minimal\hitmanpro36.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Minimal\hitmanpro36Crusader /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Minimal\hitmanpro36CrusaderBoot /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Minimal\hitmanpro37 /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Minimal\hitmanpro37.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro36.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro36Crusader /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro36CrusaderBoot /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro37 /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro37.sys /f >nul 2>&1

reg delete HKLM\System\ControlSet\Control\SafeBoot\Minimal\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Minimal\hitmanpro36.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Minimal\hitmanpro36Crusader /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Minimal\hitmanpro36CrusaderBoot /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Minimal\hitmanpro37 /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Minimal\hitmanpro37.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Network\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Network\hitmanpro36 /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Network\hitmanpro36.sys /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Network\hitmanpro36Crusader /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Network\hitmanpro36CrusaderBoot /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Network\hitmanpro37 /f >nul 2>&1
reg delete HKLM\System\ControlSet\Control\SafeBoot\Network\hitmanpro37.sys  /f >nul 2>&1

rem ******the following commands remove unnecessary temp files to reduce scan times******
@echo.
@echo ********** Removing temporary files **********
@echo.
cd c:\windows
rmdir temp /s /q >nul 2>&1
mkdir c:\Windows\Temp >nul 2>&1
del c:\windows\prefetch\*.* /f /s /q >nul 2>&1

cd %userprofile%\
rmdir cookies /s /q >nul 2>&1
mkdir cookies >nul 2>&1

cd %userprofile%\"local settings"\
rmdir temp /s /q >nul 2>&1
mkdir temp >nul 2>&1
rmdir "temporary internet files" /s /q >nul 2>&1
mkdir "temporary internet files" >nul 2>&1

cd %userprofile%\appdata\local\
rmdir temp /s /q >nul 2>&1
mkdir temp >nul 2>&1

cd %userprofile%\appdata\local\microsoft\windows\
rmdir "temporary internet files" /s /q >nul 2>&1
mkdir "temporary internet files" >nul 2>&1

cd \
del %temp%*.* /f /s /q >nul 2>&1
del %tmp%*.* /f /s /q  >nul 2>&1
del *.tmp /f /s /q 

@echo ********** All temporary files have been removed **********
