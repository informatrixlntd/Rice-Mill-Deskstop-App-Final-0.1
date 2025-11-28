@echo off
echo ============================================
echo FIXING DATABASE - RECREATING TABLE
echo ============================================
echo.
mysql -u root -p purchase_slips_db < recreate_table.sql
echo.
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Table recreated with correct schema.
    echo Now restart your backend: python backend/app.py
) else (
    echo ERROR! Check MySQL credentials.
)
pause
