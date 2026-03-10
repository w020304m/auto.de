@echo off
REM Push to GitHub - Run AFTER creating repository on GitHub

echo ========================================
echo Pushing to GitHub...
echo ========================================
echo.

git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed. Make sure you:
    echo   1. Created the repository on GitHub
    echo   2. Updated your username in git_deploy.bat
    echo   3. Ran git_deploy.bat first
    echo.
) else (
    echo.
    echo ========================================
    echo SUCCESS! Repository pushed to GitHub
    echo ========================================
    echo.
    echo Next: Deploy to Cloudflare Pages
    echo https://dash.cloudflare.com/
    echo.
)

pause
