@echo off
echo 🚀 Pushing Indian Stock AI Agent to GitHub...
echo.

cd /d "C:\Users\risha\Downloads\my-sec-ai-agent"

echo 📋 Current directory: %CD%
echo.

echo 🔧 Removing existing remote (if any)...
git remote remove origin 2>nul

echo 🔗 Adding new GitHub repository...
git remote add origin https://github.com/Rishab2469/stock-market-ai-agent.git

echo 📊 Checking git status...
git status

echo 🌿 Setting main branch...
git branch -M main

echo 🚀 Pushing to GitHub...
git push -u origin main

echo.
echo ✅ Done! Check your repository at:
echo https://github.com/Rishab2469/stock-market-ai-agent
echo.
pause
