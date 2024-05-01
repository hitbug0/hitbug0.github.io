echo off
python ./_programs/update.py

rem set port number
set port=8080
rem set /p port=Enter port number:

rem Starting HTTP server
start cmd /c "python -m http.server %port%"

rem Waiting for server to start
powershell -command "& {Start-Sleep -Seconds 0.2}"

rem Opening http://localhost:%port%/ in Chrome
start chrome.exe http://localhost:%port%/

pause