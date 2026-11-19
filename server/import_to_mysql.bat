@echo off
echo ============================================================
echo Importing Kitchen Intelligence Database to phpMyAdmin / MySQL
echo ============================================================

REM Check if XAMPP MySQL exists
if not exist "C:\xampp\mysql\bin\mysql.exe" (
    echo [ERROR] C:\xampp\mysql\bin\mysql.exe not found.
    echo Please make sure XAMPP is installed in C:\xampp.
    pause
    exit /b 1
)

REM Test MySQL connection
"C:\xampp\mysql\bin\mysql.exe" -u root -e "SHOW DATABASES;" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Cannot connect to MySQL server.
    echo.
    echo 1. Open your XAMPP Control Panel.
    echo 2. Click "Start" on MySQL (and Apache).
    echo 3. Run this batch file again!
    echo.
    pause
    exit /b 1
)

echo [1/2] Importing 26 tables and all data into MySQL...
"C:\xampp\mysql\bin\mysql.exe" -u root < "%~dp0kitchen_intelligence_mysql.sql"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Import failed. Check the error message above.
    pause
    exit /b 1
)

echo [2/2] Import completed successfully!
echo.
echo ============================================================
echo Open phpMyAdmin (http://localhost/phpmyadmin) in your browser.
echo You will now see 'kitchen_intelligence' with all 26 tables!
echo ============================================================
echo.
pause

