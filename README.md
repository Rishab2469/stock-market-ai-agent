# 🇮🇳 Indian Stock AI + Sentiment Analysis Agent (NSE/BSE)

An advanced AI-powered agent that combines **professional AI analysis with real-time news sentiment** to analyze Indian stocks listed on NSE/BSE and provide intelligent buy/sell/hold recommendations.

## ✨ Key Features

### 🤖 **Hybrid AI + Sentiment Fusion**
- **Groq AI Analysis (70%)**: Professional-grade stock analysis using Llama 3.1 models
- **News Sentiment Analysis (30%)**: Real-time sentiment from Indian financial news
- **Intelligent Fusion**: Combines AI reasoning with market sentiment for superior accuracy

### 📰 **Enhanced Indian News Collection**
- **Multi-source News**: Economic Times, MoneyControl, Business Standard, LiveMint
- **Real-time Sentiment**: FinBERT-based sentiment analysis optimized for financial news
- **Indian Market Focus**: Specialized for NSE/BSE listed companies

### 📊 **Comprehensive Analysis**
- **Technical Analysis**: RSI, volume, price momentum, moving averages
- **Fundamental Screening**: Market cap, P/E ratio, beta, volatility
- **Sector-wise Analysis**: 11 major Indian sectors including Defence with up to 25 stocks each
- **Risk Assessment**: Multi-factor risk evaluation

### 🎯 **Interactive Web Dashboard**
- **Sector Heatmaps**: Visual comparison of sector performance
- **Stock Details**: Comprehensive analysis including AI reasoning
- **Real-time Updates**: Live data with hybrid analysis transparency
- **Mobile Responsive**: Works on all devices

## 🚀 Quick Start

### 1. **Clone the repository**
```bash
git clone https://github.com/Rishab2469/stock-market-ai-agent.git
cd stock-market-ai-agent
```

### 2. **Create virtual environment** (Recommended)
```bash
python -m venv stock_agent_env
# Windows
stock_agent_env\Scripts\activate
# Linux/Mac
source stock_agent_env/bin/activate
```

### 3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Set up API keys** (Required)
```bash
cp .env.example .env
```

Edit `.env` file and add your API keys:
```env
# Required for AI analysis
GROQ_API_KEY=your_groq_api_key_here

# Required for news sentiment
NEWS_API_KEY=your_news_api_key_here
```

**Get your free API keys:**
- **🤖 Groq AI**: https://console.groq.com/ (Free tier: 30 requests/minute)
- **📰 NewsAPI**: https://newsapi.org/ (Free tier: 1000 requests/day)

### 5. **Run the application**
```bash
python app.py
```

### 6. **Open your browser**
Navigate to: http://127.0.0.1:5000

### 7. **Start analyzing!**
- Select any sector (Banking, IT, Energy, etc.)
- View AI + Sentiment fusion analysis
- Click on stocks for detailed breakdown
- See transparent hybrid scoring

## 🧠 How the AI + Sentiment Fusion Works

### 🔄 **Hybrid Analysis Pipeline**

#### **Step 1: Multi-Source Data Collection**
- **📊 Stock Data**: Real-time prices, technical indicators (Yahoo Finance)
- **📰 News Data**: Indian financial news from 4+ sources (NewsAPI + scraping)
- **🏢 Fundamental Data**: Market cap, P/E ratio, sector classification

#### **Step 2: AI Analysis (70% Weight)**
- **🤖 Groq AI**: Llama 3.1-70B analyzes fundamentals, technicals, and market context
- **🇮🇳 Indian Market Focus**: AI understands NSE/BSE dynamics and regulations
- **📈 Professional Reasoning**: Generates investment thesis with catalysts and risks

#### **Step 3: Sentiment Analysis (30% Weight)**
- **📰 News Processing**: FinBERT analyzes headlines and content
- **🎯 Indian Sources**: Economic Times, MoneyControl, Business Standard
- **📊 Sentiment Scoring**: -1 (very negative) to +1 (very positive)

#### **Step 4: Intelligent Fusion**
```
Hybrid Score = (AI Score × 0.7) + (Sentiment Score × 0.3) + Modifiers

Modifiers:
+ Strong positive news (5+ articles, sentiment > 0.2): +5 points
+ AI-Technical alignment: +2 points
- Strong negative news (5+ articles, sentiment < -0.2): -5 points
```

#### **Step 5: Enhanced Recommendations**
- **🟢 BUY**: Score ≥ 60 with AI + sentiment support
- **🟡 HOLD**: Score 45-60 or mixed signals
- **🔴 SELL**: Score < 45 or negative sentiment override

### 🎯 **Analysis Transparency**
- **Analysis Source**: Shows "AI+Sentiment", "AI Only", or "Rule-based"
- **Component Breakdown**: See AI base score vs sentiment boost
- **Reasoning**: Combined AI thesis with sentiment context

## Configuration

Edit `config.py` to customize:

```python
# Filtering parameters
MIN_SENTIMENT_SCORE = 0.1      # Minimum positive sentiment
MIN_VOLUME_RATIO = 1.5         # Minimum volume vs average
MAX_PRICE_CHANGE = 0.05        # Maximum daily change (5%)
MIN_MARKET_CAP = 1000000000    # Minimum market cap ($1B)

# Stock universe
STOCK_SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', ...]  # Add your stocks

# Risk management
MAX_RECOMMENDATIONS = 10        # Max buy recommendations
RISK_TOLERANCE = 'medium'       # low, medium, high
```

## API Endpoints

- `GET /api/recommendations` - Get all recommendations
- `GET /api/recommendations/BUY` - Get buy recommendations only
- `GET /api/stats` - Get summary statistics
- `GET /api/charts/sentiment-distribution` - Sentiment chart data
- `GET /api/charts/recommendation-distribution` - Recommendation chart data

## Risk Disclaimer

⚠️ **Important**: This tool is for educational and research purposes only. It is NOT financial advice. Always:
- Do your own research
- Consult with financial advisors
- Consider your risk tolerance
- Never invest more than you can afford to lose

## Dependencies

- **Flask**: Web framework
- **yfinance**: Stock data
- **newsapi-python**: News data
- **transformers**: AI sentiment analysis
- **textblob**: Backup sentiment analysis
- **pandas/numpy**: Data processing
- **plotly**: Interactive charts

## Troubleshooting

### Common Issues

1. **No news data**: Check your NewsAPI key in `.env`
2. **Stock data errors**: Yahoo Finance may be temporarily unavailable
3. **Slow analysis**: First run downloads AI models (normal)
4. **Memory issues**: Reduce stock symbols list in config

### Performance Tips

- Use NewsAPI key for better news coverage
- Reduce `STOCK_SYMBOLS` list for faster analysis
- Increase `NEWS_LOOKBACK_DAYS` for more comprehensive analysis
- Cache results are stored for 30 minutes

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration options
3. Open an issue on GitHub
