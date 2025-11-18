@echo off
:: Script: Geforce-Hybrid-Capture.bat
setlocal enabledelayedexpansion

:: Change to the script's directory to ensure proper path resolution
cd /d "%~dp0"

:MAIN_MENU
cls
echo ===============================================================================
echo    Geforce-Hybrid-Capture: Batch Menu
echo ===============================================================================
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo    1) Launch Geforce-Hybrid-Capture
echo.
echo    2) Install Requirements
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo -------------------------------------------------------------------------------
set /p choice="Selection; Menu Options = 1-2, Quit Program = Q: "

if /i "%choice%"=="1" call :LAUNCH
if /i "%choice%"=="2" call :INSTALL
if /i "%choice%"=="Q" call :QUIT
if /i "%choice%"=="1" goto MAIN_MENU
if /i "%choice%"=="2" goto MAIN_MENU
if /i "%choice%"=="Q" exit /b 0
echo Invalid selection. Please try again.
pause
goto MAIN_MENU

:LAUNCH
cls
echo ===============================================================================
echo    Launching Geforce-Hybrid-Capture
echo ===============================================================================
echo.
echo Starting application...
python launcher.py
echo.
pause
goto :eof

:INSTALL
cls
echo ===============================================================================
echo    Installing Requirements
echo ===============================================================================
echo.
echo Installing Python dependencies...
python installer.py
echo.
echo Installation complete.
pause
goto :eof

:QUIT
cls
echo ===============================================================================
echo    Exiting Program
echo ===============================================================================
echo.
echo Exiting program...
echo Thank you for using Geforce-Hybrid-Capture.
echo.
timeout /t 2 /nobreak >nul
goto :eof