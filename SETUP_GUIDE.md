# Indian Stock News Analysis Agent (NSE/BSE) - Setup Guide

## 🚀 Quick Start

Your Indian stock filtering agent is now **LIVE** and running! Here's how to use it:

### Current Status
✅ **Virtual Environment**: Created and activated
✅ **Dependencies**: Core packages installed
✅ **Web Application**: Running at http://127.0.0.1:5000
✅ **Basic Functionality**: Stock data fetching and sentiment analysis working

## 📋 What You Have

### 1. **Live Web Dashboard**
- **URL**: http://127.0.0.1:5000
- **Features**:
  - Real-time stock analysis
  - Buy/Sell/Hold recommendations
  - Interactive charts and statistics
  - News sentiment analysis
  - Risk assessment

### 2. **Core Components**
- `app.py` - Flask web application
- `stock_filter.py` - Main analysis engine
- `sentiment_analyzer.py` - News sentiment analysis
- `stock_data.py` - Stock data collection
- `news_collector.py` - News data collection
- `config.py` - Configuration settings

### 3. **Command Line Tools**
- `start_agent.py` - Quick start script
- `run_analysis.py` - Command line analysis
- `test_agent.py` - Test suite

## 🔧 Setup Commands

### Activate Virtual Environment
```bash
# Windows
stock_agent_env\Scripts\activate

# Then run any of these:
python app.py                 # Web application
python start_agent.py         # Interactive start
python run_analysis.py        # Command line analysis
```

## 📊 How It Works

### 1. **Data Collection**
- Fetches real-time stock prices from Yahoo Finance
- Collects financial news from multiple sources
- Gathers fundamental data (P/E ratio, market cap, etc.)

### 2. **Analysis Pipeline**
- **Sentiment Analysis**: Analyzes news using TextBlob (FinBERT optional)
- **Technical Analysis**: RSI, volume ratios, price momentum
- **Fundamental Screening**: Market cap, volatility, beta

### 3. **Scoring System**
- **Sentiment Component (40%)**: News sentiment analysis
- **Technical Component (30%)**: Technical indicators
- **Fundamental Component (20%)**: Company fundamentals
- **News Coverage Component (10%)**: Article count and recency

### 4. **Recommendations**
- **BUY**: Score ≥ 55 with positive sentiment
- **HOLD**: Score 45-55 or mixed signals
- **SELL**: Score < 45 or negative sentiment

## 🎯 Current Indian Stock Universe

The agent analyzes these NSE/BSE stocks by default:
```
Large Cap: RELIANCE, TCS, HDFCBANK, INFY, HINDUNILVR, ICICIBANK,
          KOTAKBANK, BHARTIARTL, ITC, SBIN, BAJFINANCE, LICI, LT

Mid Cap:   ADANIPORTS, ADANIENT, TATAMOTORS, JSWSTEEL, INDUSINDBK,
          BAJAJFINSV, DRREDDY, CIPLA, GRASIM, HINDALCO

Tech:      HCLTECH, ASIANPAINT, WIPRO, TECHM, MINDTREE, MPHASIS
```

## ⚙️ Configuration

### Basic Settings (config.py)
```python
MIN_SENTIMENT_SCORE = 0.1      # Minimum positive sentiment
MIN_VOLUME_RATIO = 1.5         # Volume vs average
MAX_PRICE_CHANGE = 0.05        # Max daily change (5%)
MIN_MARKET_CAP = 10000000000   # Min market cap (₹100 Cr)
```

### API Keys (Optional)
Create `.env` file for enhanced features:
```bash
# Copy example file
cp .env.example .env

# Add your API keys
NEWS_API_KEY=your_newsapi_key_here
ALPHA_VANTAGE_KEY=your_alphavantage_key_here
```

## 🌐 Web Interface Features

### Dashboard Sections
1. **Summary Cards**: Buy/Sell/Hold counts, average sentiment
2. **Charts**: Sentiment distribution, recommendation breakdown
3. **Recommendations Table**: Detailed stock analysis with filtering
4. **Real-time Updates**: Refresh button for latest data

### API Endpoints
- `GET /api/recommendations` - All recommendations
- `GET /api/recommendations/BUY` - Buy recommendations only
- `GET /api/stats` - Summary statistics
- `GET /api/charts/*` - Chart data

## 📈 Usage Examples

### Web Interface
1. Open http://127.0.0.1:5000
2. View real-time recommendations
3. Filter by Buy/Sell/Hold
4. Click refresh for latest data

### Command Line
```bash
# Quick analysis
python run_analysis.py

# Specific stocks
python run_analysis.py --symbols AAPL MSFT GOOGL

# Buy recommendations only
python run_analysis.py --action BUY --limit 5

# Save to CSV
python run_analysis.py --save my_recommendations.csv
```

## 🔍 Understanding Results

### Recommendation Columns
- **Symbol**: Stock ticker
- **Price**: Current stock price
- **Change %**: Daily price change
- **Sentiment**: News sentiment (positive/negative/neutral)
- **Score**: Composite score (0-100)
- **Recommendation**: BUY/SELL/HOLD
- **Confidence**: High/Medium/Low
- **Risk**: Risk level assessment
- **Reasoning**: Why this recommendation

### Score Interpretation
- **80-100**: Strong buy with high confidence
- **60-79**: Good buy opportunity
- **40-59**: Hold or neutral
- **20-39**: Consider selling
- **0-19**: Strong sell signal

## 🚨 Important Disclaimers

⚠️ **This tool is for educational and research purposes only**

- **NOT financial advice**
- Always do your own research
- Consult with financial advisors
- Consider your risk tolerance
- Never invest more than you can afford to lose

## 🛠️ Troubleshooting

### Common Issues
1. **No data**: Check internet connection
2. **Slow performance**: Reduce stock symbols in config
3. **Memory issues**: Close other applications
4. **API errors**: Check API keys in .env file

### Performance Tips
- First run downloads data (may be slow)
- Results are cached for 30 minutes
- Use NewsAPI key for better news coverage
- Reduce stock list for faster analysis

## 📚 Next Steps

### Enhancements You Can Add
1. **Install transformers** for better sentiment analysis:
   ```bash
   pip install transformers torch
   ```

2. **Add API keys** for more news sources
3. **Customize stock list** in config.py
4. **Adjust filtering parameters** for your strategy
5. **Add more technical indicators**

### Advanced Usage
- Modify scoring weights in `stock_filter.py`
- Add new data sources in `news_collector.py`
- Customize risk assessment in `_assess_risk()`
- Add email alerts for buy signals

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the configuration options
3. Run `python test_agent.py` to diagnose problems
4. Check terminal output for error messages

---

**🎉 Congratulations! Your stock analysis agent is now live and ready to help you make informed investment decisions!**
