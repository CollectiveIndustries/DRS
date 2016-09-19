title Computer Warehouse Clean up Tool
@echo off
color 72
cls
c:
cd \

@echo.
@echo ********** Removing leftover scan results folders **********
@echo.
@echo Removing AdwCleaner 
rmdir c:\AdwCleaner /s /q >nul 2>&1
@echo.

@echo Removing JRT
rmdir c:\JRT /s /q >nul 2>&1
del %userprofile%\desktop\jrt.exe /f /s /q >nul 2>&1
@echo.

@echo Removing HitmanPro
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
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro37Crusader /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Control\SafeBoot\Network\hitmanpro37CrusaderBoot /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Enum\Root\LEGACY_HITMANPRO37 /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Services\HitmanProScheduler /f >nul 2>&1
reg delete HKLM\System\ControlSet001\Services\HitmanPro37 /f >nul 2>&1
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
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro37Crusader /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Control\SafeBoot\Network\hitmanpro37CrusaderBoot /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Enum\Root\LEGACY_HITMANPRO37 /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Services\HitmanProScheduler /f >nul 2>&1
reg delete HKLM\System\ControlSet002\Services\HitmanPro37 /f >nul 2>&1
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
reg delete HKLM\System\ControlSet\Enum\Root\LEGACY_HITMANPRO37 /f >nul 2>&1
reg delete HKLM\System\ControlSet\Services\HitmanProScheduler /f >nul 2>&1
reg delete HKLM\System\ControlSet\Services\HitmanPro37 /f >nul 2>&1
reg delete HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\HitmanPro37 /f >nul 2>&1

@echo.
@echo Removing Super Anti Spyware
rmdir c:\SUPERDelete /s /q >nul 2>&1

@echo. 
@echo Removing NPE 
rmdir c:\NPE /s /q  >nul 2>&1

@echo.
@echo Removing ComboFix
del c:\combofix.txt >nul 2>&1

@echo.
@echo Removing HerdProtect
c:
cd \
md HerdProtect
cd HerdProtect
pushd "\\nas\Tech\Infection Removal\HerdProtect\"
del *.dat /f /q /s >nul 2>&1
cd quarantine
del *.* /f /q /s >nul 2>&1
cd ..
cd cache
del *.* /f /q /s >nul 2>&1
cd ..
cd logs
del *.* /f /q /s >nul 2>&1
popd
cd\
rd HerdProtect

@echo.
@echo Emptying Recycle Bin
rd /s /q %systemdrive%\$Recycle.bin >nul 2>&1
@echo.
@echo  ********** All folders have been removed **********
@echo.
pause
