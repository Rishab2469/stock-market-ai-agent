import requests
import pandas as pd
from datetime import datetime, timedelta
from config import Config
import time
import json

# Try to import optional dependencies
try:
    from newsapi import NewsApiClient
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False
    NewsApiClient = None

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None

class EnhancedIndianNewsCollector:
    def __init__(self):
        print(f"🔍 NewsAPI available: {NEWSAPI_AVAILABLE}")
        print(f"🔑 NEWS_API_KEY configured: {'✓ YES' if Config.NEWS_API_KEY else '✗ NO'}")

        self.news_api = NewsApiClient(api_key=Config.NEWS_API_KEY) if (NEWSAPI_AVAILABLE and Config.NEWS_API_KEY) else None

        if self.news_api:
            print("✅ NewsAPI client initialized successfully")
        else:
            print("❌ NewsAPI client not initialized - will use fallback methods only")

        # Enhanced Indian financial news sources
        self.indian_news_sources = {
            'primary': [
                'economictimes.com',
                'moneycontrol.com',
                'business-standard.com',
                'livemint.com',
                'financialexpress.com'
            ],
            'secondary': [
                'bloombergquint.com',
                'cnbctv18.com',
                'zeebiz.com',
                'businesstoday.in',
                'thehindubusinessline.com'
            ],
            'specialized': [
                'investing.com',
                'tradingview.com',
                'screener.in',
                'tickertape.in'
            ]
        }

        # Company name mapping (same as before but enhanced)
        self.indian_company_names = {
            # Banking
            'HDFCBANK.NS': 'HDFC Bank', 'ICICIBANK.NS': 'ICICI Bank', 'KOTAKBANK.NS': 'Kotak Mahindra Bank',
            'SBIN.NS': 'State Bank of India', 'AXISBANK.NS': 'Axis Bank', 'INDUSINDBK.NS': 'IndusInd Bank',

            # IT
            'TCS.NS': 'Tata Consultancy Services', 'INFY.NS': 'Infosys', 'HCLTECH.NS': 'HCL Technologies',
            'WIPRO.NS': 'Wipro', 'TECHM.NS': 'Tech Mahindra',

            # Energy
            'RELIANCE.NS': 'Reliance Industries', 'ONGC.NS': 'Oil and Natural Gas Corporation',
            'BPCL.NS': 'Bharat Petroleum', 'IOC.NS': 'Indian Oil Corporation',

            # Auto
            'MARUTI.NS': 'Maruti Suzuki', 'TATAMOTORS.NS': 'Tata Motors', 'M&M.NS': 'Mahindra & Mahindra',
            'BAJAJ-AUTO.NS': 'Bajaj Auto', 'HEROMOTOCO.NS': 'Hero MotoCorp',

            # Pharma
            'SUNPHARMA.NS': 'Sun Pharmaceutical', 'DRREDDY.NS': 'Dr Reddys Laboratories', 'CIPLA.NS': 'Cipla',

            # FMCG
            'HINDUNILVR.NS': 'Hindustan Unilever', 'ITC.NS': 'ITC Limited', 'NESTLEIND.NS': 'Nestle India',

            # Defence
            'HAL.NS': 'Hindustan Aeronautics Limited', 'BEL.NS': 'Bharat Electronics Limited',
            'BEML.NS': 'BEML Limited', 'GRSE.NS': 'Garden Reach Shipbuilders',
            'COCHINSHIP.NS': 'Cochin Shipyard', 'MIDHANI.NS': 'Mishra Dhatu Nigam',
            'ORDNFAC.NS': 'Ordnance Factory Board', 'MAZAGON.NS': 'Mazagon Dock Shipbuilders',
            'BHEL.NS': 'Bharat Heavy Electricals', 'DATAPATTNS.NS': 'Data Patterns',

            # Add more as needed...
        }

    def get_stock_news_enhanced(self, symbol, days_back=7):
        """Enhanced news collection for Indian stocks"""
        all_articles = []
        print(f"📰 Collecting news for {symbol}...")

        # Method 1: NewsAPI with Indian sources
        if self.news_api:
            print(f"   🔍 Method 1: NewsAPI...")
            newsapi_articles = self._get_newsapi_indian(symbol, days_back)
            all_articles.extend(newsapi_articles)
            print(f"   ✓ NewsAPI: {len(newsapi_articles)} articles")
        else:
            print(f"   ⚠️  Method 1: NewsAPI not available")

        # Method 2: Yahoo Finance (reliable fallback)
        print(f"   🔍 Method 2: Yahoo Finance...")
        yahoo_articles = self._get_yahoo_news(symbol)
        all_articles.extend(yahoo_articles)
        print(f"   ✓ Yahoo Finance: {len(yahoo_articles)} articles")

        # Method 3: MoneyControl scraping (Indian-specific)
        print(f"   🔍 Method 3: MoneyControl...")
        mc_articles = self._scrape_moneycontrol(symbol)
        all_articles.extend(mc_articles)
        print(f"   ✓ MoneyControl: {len(mc_articles)} articles")

        # Method 4: Economic Times scraping
        print(f"   🔍 Method 4: Economic Times...")
        et_articles = self._scrape_economic_times(symbol)
        all_articles.extend(et_articles)
        print(f"   ✓ Economic Times: {len(et_articles)} articles")

        print(f"📊 Total articles for {symbol}: {len(all_articles)}")
        return all_articles

    def _get_newsapi_indian(self, symbol, days_back):
        """Enhanced NewsAPI search for Indian stocks"""
        articles = []

        try:
            company_name = self.indian_company_names.get(symbol, symbol.replace('.NS', ''))

            # Multiple search strategies
            search_queries = [
                f'"{company_name}"',
                f'{company_name} stock',
                f'{company_name} shares',
                f'{symbol.replace(".NS", "")} NSE',
                f'{symbol.replace(".NS", "")} BSE'
            ]

            for query in search_queries[:2]:  # Limit to avoid API quota
                try:
                    response = self.news_api.get_everything(
                        q=query,
                        from_param=(datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d'),
                        to=datetime.now().strftime('%Y-%m-%d'),
                        language='en',
                        sort_by='relevancy',
                        page_size=10,
                        domains=','.join(self.indian_news_sources['primary'])
                    )

                    if response['status'] == 'ok':
                        for article in response['articles']:
                            articles.append({
                                'title': article['title'],
                                'description': article['description'],
                                'content': article['content'],
                                'url': article['url'],
                                'published_at': article['publishedAt'],
                                'source': article['source']['name'],
                                'symbol': symbol,
                                'method': 'NewsAPI'
                            })

                except Exception as e:
                    print(f"NewsAPI query error for {query}: {e}")

        except Exception as e:
            print(f"NewsAPI error for {symbol}: {e}")

        return articles

    def _get_yahoo_news(self, symbol):
        """Yahoo Finance news (reliable for Indian stocks)"""
        articles = []

        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            news = ticker.news

            for item in news[:10]:
                articles.append({
                    'title': item.get('title', ''),
                    'description': item.get('summary', ''),
                    'content': item.get('summary', ''),
                    'url': item.get('link', ''),
                    'published_at': datetime.fromtimestamp(item.get('providerPublishTime', 0)).isoformat(),
                    'source': item.get('publisher', 'Yahoo Finance'),
                    'symbol': symbol,
                    'method': 'Yahoo Finance'
                })

        except Exception as e:
            print(f"Yahoo Finance error for {symbol}: {e}")

        return articles

    def _scrape_moneycontrol(self, symbol):
        """Scrape MoneyControl for Indian stock news"""
        articles = []

        if not BS4_AVAILABLE:
            print("BeautifulSoup not available, skipping MoneyControl scraping")
            return articles

        try:
            # MoneyControl uses different symbol format
            mc_symbol = symbol.replace('.NS', '')

            # Search URL for MoneyControl
            search_url = f"https://www.moneycontrol.com/news/tags/{mc_symbol.lower()}.html"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find news articles (MoneyControl structure)
                news_items = soup.find_all('div', class_='news_item')[:5]  # Limit to 5

                for item in news_items:
                    try:
                        title_elem = item.find('a')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            url = title_elem.get('href')

                            # Make URL absolute if relative
                            if url and not url.startswith('http'):
                                url = f"https://www.moneycontrol.com{url}"

                            articles.append({
                                'title': title,
                                'description': title,  # MoneyControl doesn't always have separate description
                                'content': title,
                                'url': url,
                                'published_at': datetime.now().isoformat(),
                                'source': 'MoneyControl',
                                'symbol': symbol,
                                'method': 'MoneyControl Scraping'
                            })
                    except Exception as e:
                        continue

        except Exception as e:
            print(f"MoneyControl scraping error for {symbol}: {e}")

        return articles

    def _scrape_economic_times(self, symbol):
        """Scrape Economic Times for Indian stock news"""
        articles = []

        if not BS4_AVAILABLE:
            print("BeautifulSoup not available, skipping Economic Times scraping")
            return articles

        try:
            company_name = self.indian_company_names.get(symbol, symbol.replace('.NS', ''))

            # Economic Times search
            search_url = f"https://economictimes.indiatimes.com/topic/{company_name.replace(' ', '-').lower()}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find news articles (ET structure)
                news_items = soup.find_all('div', class_='eachStory')[:5]

                for item in news_items:
                    try:
                        title_elem = item.find('h3')
                        if title_elem:
                            link_elem = title_elem.find('a')
                            if link_elem:
                                title = link_elem.get_text(strip=True)
                                url = link_elem.get('href')

                                if url and not url.startswith('http'):
                                    url = f"https://economictimes.indiatimes.com{url}"

                                articles.append({
                                    'title': title,
                                    'description': title,
                                    'content': title,
                                    'url': url,
                                    'published_at': datetime.now().isoformat(),
                                    'source': 'Economic Times',
                                    'symbol': symbol,
                                    'method': 'ET Scraping'
                                })
                    except Exception as e:
                        continue

        except Exception as e:
            print(f"Economic Times scraping error for {symbol}: {e}")

        return articles

    def get_indian_market_news(self):
        """Get general Indian market news from multiple sources"""
        articles = []

        # NewsAPI for market news
        if self.news_api:
            try:
                response = self.news_api.get_everything(
                    q='Sensex OR Nifty OR "Indian stock market" OR BSE OR NSE',
                    language='en',
                    sort_by='publishedAt',
                    page_size=15,
                    domains=','.join(self.indian_news_sources['primary'])
                )

                if response['status'] == 'ok':
                    for article in response['articles']:
                        articles.append({
                            'title': article['title'],
                            'description': article['description'],
                            'content': article['content'],
                            'url': article['url'],
                            'published_at': article['publishedAt'],
                            'source': article['source']['name'],
                            'symbol': 'MARKET',
                            'method': 'NewsAPI Market'
                        })
            except Exception as e:
                print(f"Market news error: {e}")

        return articles

    def collect_all_news_enhanced(self, symbols):
        """Enhanced news collection for all symbols"""
        all_news = []

        print("Collecting Indian market news...")
        market_news = self.get_indian_market_news()
        all_news.extend(market_news)

        print(f"Collecting enhanced news for {len(symbols)} Indian stocks...")
        for i, symbol in enumerate(symbols):
            print(f"Processing {symbol} ({i+1}/{len(symbols)}) with multiple sources...")

            stock_news = self.get_stock_news_enhanced(symbol, Config.NEWS_LOOKBACK_DAYS)
            all_news.extend(stock_news)

            # Rate limiting to be respectful to websites
            time.sleep(0.2)

            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(symbols)} stocks...")

        print(f"Total articles collected: {len(all_news)}")
        return pd.DataFrame(all_news)
