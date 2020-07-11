@echo off

set "basepath=%appdata%\notifier"
set "exepath=%basepath%\notifier.exe"
set "linkpath=%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\notifier-startup.lnk"
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"


xcopy /S /I /Y "notifier" "%basepath%"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%linkpath%" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%exepath%" >> %SCRIPT%
echo oLink.WorkingDirectory = "%basepath%" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%
