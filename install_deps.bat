@echo off
echo 🔧 Installing Stock Analysis Dependencies...
echo.

REM Activate virtual environment
call stock_agent_env\Scripts\activate.bat

echo 📦 Installing required packages...
pip install pandas yfinance requests numpy

echo.
echo 📦 Installing optional AI packages...
pip install transformers torch --index-url https://download.pytorch.org/whl/cpu

echo.
echo 🧪 Testing installation...
python -c "import pandas, yfinance, requests, numpy; print('✅ All required packages installed successfully!')"

echo.
echo 🚀 Running dependency installer...
python install_dependencies.py

echo.
echo ✅ Installation complete!
echo.
echo 🚀 Next steps:
echo 1. Get your free Groq API key from: https://console.groq.com/
echo 2. Add it to .env file: GROQ_API_KEY=your_key_here
echo 3. Test setup: python test_ai_integration.py
echo 4. Start app: python app.py
echo.
pause
