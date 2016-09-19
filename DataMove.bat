chcp 65001
title Organizing Recovered Data
@echo off
color 4F
cls
@echo.
@echo. 
@echo                                           ╔══════════════════════════════════╗
@echo                                           ║                                  ║
@echo                                           ║       ***** Caution *****        ║
@echo                                           ║                                  ║
@echo                                           ║ Copy this batch file to the root ║
@echo                                           ║ of the drive you are organizing. ║
@echo                                           ║  Run it from command line ONLY!  ║
@echo                                           ║                                  ║
@echo                                           ╚══════════════════════════════════╝
@echo.
@echo.
@echo.
@echo.
@echo                                       Are you sure you want to arrange the files in
@echo.
@echo. 
echo                                                    %~dp0 ?
@echo.
@echo.
@echo.
@echo.
@echo.
@echo.
@echo.
@echo.
@echo.
@echo.
pause

if exist *.avi md avi
if exist *.avi move *.avi avi\
if exist *.bmp md bmp
if exist *.bmp move *.bmp bmp\
if exist *.doc md doc
if exist *.doc move *.doc doc\
if exist *.docx md doc >nul 2>&1
if exist *.docx move *.docx doc\
if exist *.flv md flv
if exist *.flv move *.flv flv\
if exist *.gif md gif
if exist *.gif move *.gif gif\
if exist *.ics md ics
if exist *.ics move *.ics ics\
if exist *.jpg md jpg
if exist *.jpg move *.jpg jpg\
if exist *.m4a md m4a
if exist *.m4a move *.m4a m4a\
if exist *.m4v md m4v
if exist *.m4v move *.m4v m4v\
if exist *.mp3 md mp3
if exist *.mp3 move *.mp3 mp3\
if exist *.mp4 md mp4
if exist *.mp4 move *.mp4 mp4\
if exist *.pdf md pdf
if exist *.pdf move *.pdf pdf\
if exist *.png md png
if exist *.png move *.png png\
if exist *.ppt md ppt
if exist *.ppt move *.ppt ppt\
if exist *.qdf md qdf
if exist *.qdf move *.qdf gdf\
if exist *.qdp md qdp
if exist *.qdp move *.qdp qdp\
if exist *.qpw md qpw
if exist *.qpw move *.qpw qpw\
if exist *.tif md tif
if exist *.tif move *.tif tif\
if exist *.wmv md wmv
if exist *.wmv move *.wmv wmv\
if exist *.xls md xls
if exist *.xls move *.xls xls\
if exist *.xlsx md xls >nul 2>&1
if exist *.xlsx move *.xlsx xls\
if exist *.xml md xml
if exist *.xml move *.xml xml\
if exist *.zip md zip
if exist *.7z move *.7z zip\
if exist *.zip move *.zip zip\

md misc >nul 2>&1
for %%x in (*.*) do if /I not %%x==datamove.bat echo Moving %~dp0%%x & move %%x misc\
@echo
pause
rem @echo.
rem @echo  ********** All files have been moved into folders **********
rem @echo.
@echo.