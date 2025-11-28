@echo off
echo ================================================================
echo DATABASE SCHEMA MIGRATION
echo ================================================================
echo.
echo This will update your database to fix the "Unknown column" error
echo.
echo IMPORTANT: Make sure MySQL is running!
echo.
pause

echo.
echo Running migration...
echo.

mysql -u root -p purchase_slips_db < migration_schema_update.sql

echo.
echo ================================================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Migration completed successfully!
    echo.
    echo Next steps:
    echo 1. Restart your backend server
    echo 2. Try creating a slip again
) else (
    echo ERROR! Migration failed.
    echo.
    echo Please check:
    echo - Is MySQL running?
    echo - Is the password correct?
    echo - Does the database exist?
)
echo ================================================================
echo.
pause
