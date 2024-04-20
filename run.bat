@echo off

python ./_programs/make_posts.py
python ./_programs/make_index.py
python ./_programs/add_ad_to_posts.py
python ./_programs/make_sitemap.py


rem set port number
set port=8080
rem set /p port=Enter port number:

rem Starting HTTP server
start cmd /c "python -m http.server %port%"

rem Waiting for server to start
powershell -command "& {Start-Sleep -Seconds 0.2}"

rem Opening http://localhost:%port%/ in Chrome
start chrome.exe http://localhost:%port%/