@echo off
cd /d "%~dp0"
echo ========================================================
echo Pushing FileForge to https://github.com/AIENG-DEV/FileForge.git
echo ========================================================
echo.
git push -u origin main
echo.
pause

