@echo off
REM Git Deployment Script for Handwerker Ratgeber
REM Usage: Update YOUR_USERNAME below, then run this script

echo ========================================
echo Handwerker Ratgeber - Git Deployment
echo ========================================
echo.

REM ====== 配置区域 - 请修改为你的信息 ======https://github.com/w020304m/auto.de.git
set USERNAME=wm
set REPO=handwerker-ratgeber
REM set REPO=auto.de
set REMOTE_URL=https://github.com/%USERNAME%/%REPO%.git
REM ========================================

REM 检查是否已配置
if "%USERNAME%"=="YOUR_USERNAME" (
    echo ERROR: 请先编辑此文件，将 YOUR_USERNAME 替换为你的GitHub用户名
    echo.
    pause
    exit /b 1
)

echo 1. Initializing Git repository...
git init
if errorlevel 1 goto error

echo.
echo 2. Adding files...
git add output/ .gitignore
if errorlevel 1 goto error

echo.
echo 3. Creating commit...
git commit -m "Phase 1: Deploy 375 pages"
if errorlevel 1 goto error

echo.
echo 4. Adding remote...
git remote add origin %REMOTE_URL%
if errorlevel 1 goto error

echo.
echo ========================================
echo Ready to push!
echo ========================================
echo.
echo Next steps:
echo   1. Create repository on GitHub: https://github.com/new
echo   2. Repository name: %REPO%
echo   3. Run: git push -u origin main
echo.
echo Or run the included push_to_github.bat script
echo.
pause
exit /b 0

:error
echo.
echo ERROR: Command failed. Please check the error message above.
pause
exit /b 1
