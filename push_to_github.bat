@echo off
echo 🚀 Publishing Indian Stock AI Agent to GitHub...
echo.

cd /d "C:\Users\risha\Downloads\my-sec-ai-agent"

echo 📋 Current directory: %CD%
echo.

echo 📦 Adding all files...
git add .

echo 📝 Committing changes...
git commit -m "🛡️ Defence Sector + Production Ready Release - Complete Indian Stock AI Agent with 11 sectors, AI+Sentiment fusion, comprehensive technical analysis"

echo 🔧 Removing existing remote (if any)...
git remote remove origin 2>nul

echo 🔗 Adding GitHub repository...
git remote add origin https://github.com/Rishab2469/stock-market-ai-agent.git

echo 📊 Checking git status...
git status

echo 🌿 Setting main branch...
git branch -M main

echo 🚀 Pushing to GitHub...
git push -u origin main

echo.
echo ✅ SUCCESS! Your repository is now live at:
echo 🔗 https://github.com/Rishab2469/stock-market-ai-agent
echo.
echo 🎉 FEATURES PUBLISHED:
echo ✅ 11 Sectors including Defence
echo ✅ AI + Sentiment Fusion Analysis
echo ✅ 270+ Indian Stocks (NSE/BSE)
echo ✅ Professional Web Dashboard
echo ✅ Complete Technical Analysis
echo ✅ Multi-source News Integration
echo.
pause
