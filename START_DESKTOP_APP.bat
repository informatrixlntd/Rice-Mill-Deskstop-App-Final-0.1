@echo off
title Rice Mill Desktop Application
color 0A

echo.
echo ========================================
echo    RICE MILL DESKTOP APPLICATION
echo ========================================
echo.
echo Starting application...
echo.

echo [1/2] Starting backend server...
cd backend
start "Rice Mill Backend" cmd /k python app.py

timeout /t 5 /nobreak > nul

echo [2/2] Starting desktop application...
cd ../desktop
start "Rice Mill Desktop" cmd /k npm start

echo.
echo ========================================
echo    APPLICATION STARTED SUCCESSFULLY!
echo ========================================
echo.
echo The desktop application will open shortly.
echo.
echo To stop the application:
echo 1. Close the desktop window
echo 2. Close the backend command window
echo.
pause
