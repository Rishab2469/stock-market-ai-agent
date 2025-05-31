# PowerShell script to publish to GitHub with Personal Access Token
# Usage: .\publish_with_token.ps1

Write-Host "🚀 Publishing Indian Stock AI Agent to GitHub..." -ForegroundColor Green
Write-Host ""

# Change to project directory
Set-Location "C:\Users\risha\Downloads\my-sec-ai-agent"
Write-Host "📋 Current directory: $(Get-Location)" -ForegroundColor Yellow

# Check if git is available
try {
    git --version | Out-Null
    Write-Host "✅ Git is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/" -ForegroundColor Yellow
    exit 1
}

# Get Personal Access Token
Write-Host ""
Write-Host "🔐 GitHub Authentication Required" -ForegroundColor Cyan
Write-Host "You need a Personal Access Token (PAT) to push to GitHub" -ForegroundColor Yellow
Write-Host ""
Write-Host "To create a PAT:" -ForegroundColor White
Write-Host "1. Go to GitHub.com → Settings → Developer settings → Personal access tokens" -ForegroundColor White
Write-Host "2. Generate new token (classic)" -ForegroundColor White
Write-Host "3. Select 'repo' scope" -ForegroundColor White
Write-Host "4. Copy the generated token" -ForegroundColor White
Write-Host ""

$token = Read-Host "Enter your Personal Access Token (it will be hidden)" -AsSecureString
$tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($token))

if ([string]::IsNullOrWhiteSpace($tokenPlain)) {
    Write-Host "❌ No token provided. Exiting..." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Adding files to git..." -ForegroundColor Yellow
git add .

Write-Host "📝 Committing changes..." -ForegroundColor Yellow
git commit -m "🛡️ Defence Sector + Production Ready Release - Complete Indian Stock AI Agent"

Write-Host "🔧 Setting up remote repository..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/Rishab2469/stock-market-ai-agent.git

Write-Host "🌿 Setting main branch..." -ForegroundColor Yellow
git branch -M main

Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow

# Create URL with token for authentication
$repoUrl = "https://${tokenPlain}@github.com/Rishab2469/stock-market-ai-agent.git"

try {
    git push -u origin main --repo=$repoUrl
    Write-Host ""
    Write-Host "✅ SUCCESS! Repository published to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 Your repository is now live at:" -ForegroundColor Cyan
    Write-Host "https://github.com/Rishab2469/stock-market-ai-agent" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 FEATURES PUBLISHED:" -ForegroundColor Green
    Write-Host "✅ 11 Sectors including Defence" -ForegroundColor White
    Write-Host "✅ AI + Sentiment Fusion Analysis" -ForegroundColor White
    Write-Host "✅ 270+ Indian Stocks (NSE/BSE)" -ForegroundColor White
    Write-Host "✅ Professional Web Dashboard" -ForegroundColor White
    Write-Host "✅ Complete Technical Analysis" -ForegroundColor White
    Write-Host "✅ Multi-source News Integration" -ForegroundColor White
} catch {
    Write-Host "❌ Failed to push to GitHub" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Check your Personal Access Token" -ForegroundColor White
    Write-Host "2. Ensure the repository exists on GitHub" -ForegroundColor White
    Write-Host "3. Verify your internet connection" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
