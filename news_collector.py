import requests
import pandas as pd
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from config import Config
import time

class NewsCollector:
    def __init__(self):
        self.news_api = NewsApiClient(api_key=Config.NEWS_API_KEY) if Config.NEWS_API_KEY else None

        # Comprehensive Indian company name mapping for better news search
        self.indian_company_names = {
            # Banking
            'HDFCBANK.NS': 'HDFC Bank', 'ICICIBANK.NS': 'ICICI Bank', 'KOTAKBANK.NS': 'Kotak Mahindra Bank',
            'SBIN.NS': 'State Bank of India', 'AXISBANK.NS': 'Axis Bank', 'INDUSINDBK.NS': 'IndusInd Bank',
            'FEDERALBNK.NS': 'Federal Bank', 'BANDHANBNK.NS': 'Bandhan Bank', 'IDFCFIRSTB.NS': 'IDFC First Bank',
            'PNB.NS': 'Punjab National Bank', 'BANKBARODA.NS': 'Bank of Baroda', 'CANBK.NS': 'Canara Bank',

            # Finance & NBFC
            'BAJFINANCE.NS': 'Bajaj Finance', 'BAJAJFINSV.NS': 'Bajaj Finserv', 'LICI.NS': 'Life Insurance Corporation',
            'SBILIFE.NS': 'SBI Life Insurance', 'HDFCLIFE.NS': 'HDFC Life Insurance', 'ICICIGI.NS': 'ICICI General Insurance',
            'MUTHOOTFIN.NS': 'Muthoot Finance', 'CHOLAFIN.NS': 'Cholamandalam Investment', 'SHRIRAMFIN.NS': 'Shriram Finance',

            # Information Technology
            'TCS.NS': 'Tata Consultancy Services', 'INFY.NS': 'Infosys', 'HCLTECH.NS': 'HCL Technologies',
            'WIPRO.NS': 'Wipro', 'TECHM.NS': 'Tech Mahindra', 'LTI.NS': 'LTI Mindtree', 'MINDTREE.NS': 'Mindtree',
            'MPHASIS.NS': 'Mphasis', 'LTTS.NS': 'L&T Technology Services', 'COFORGE.NS': 'Coforge',
            'PERSISTENT.NS': 'Persistent Systems', 'OFSS.NS': 'Oracle Financial Services',

            # FMCG & Consumer
            'HINDUNILVR.NS': 'Hindustan Unilever', 'ITC.NS': 'ITC Limited', 'NESTLEIND.NS': 'Nestle India',
            'BRITANNIA.NS': 'Britannia Industries', 'DABUR.NS': 'Dabur India', 'GODREJCP.NS': 'Godrej Consumer Products',
            'MARICO.NS': 'Marico', 'COLPAL.NS': 'Colgate Palmolive', 'EMAMI.NS': 'Emami', 'TATACONSUM.NS': 'Tata Consumer Products',

            # Automotive
            'MARUTI.NS': 'Maruti Suzuki', 'TATAMOTORS.NS': 'Tata Motors', 'M&M.NS': 'Mahindra & Mahindra',
            'BAJAJ-AUTO.NS': 'Bajaj Auto', 'HEROMOTOCO.NS': 'Hero MotoCorp', 'EICHERMOT.NS': 'Eicher Motors',
            'TVSMOTORS.NS': 'TVS Motor Company', 'ASHOKLEY.NS': 'Ashok Leyland', 'BHARATFORG.NS': 'Bharat Forge',
            'MOTHERSUMI.NS': 'Motherson Sumi Systems', 'BOSCHLTD.NS': 'Bosch Limited', 'MRF.NS': 'MRF Limited',

            # Pharmaceuticals
            'SUNPHARMA.NS': 'Sun Pharmaceutical', 'DRREDDY.NS': 'Dr Reddys Laboratories', 'CIPLA.NS': 'Cipla',
            'DIVISLAB.NS': 'Divis Laboratories', 'BIOCON.NS': 'Biocon', 'LUPIN.NS': 'Lupin', 'AUROPHARMA.NS': 'Aurobindo Pharma',
            'CADILAHC.NS': 'Cadila Healthcare', 'TORNTPHARM.NS': 'Torrent Pharmaceuticals', 'GLENMARK.NS': 'Glenmark Pharmaceuticals',

            # Energy, Oil & Gas
            'RELIANCE.NS': 'Reliance Industries', 'ONGC.NS': 'Oil and Natural Gas Corporation', 'BPCL.NS': 'Bharat Petroleum',
            'IOC.NS': 'Indian Oil Corporation', 'HINDPETRO.NS': 'Hindustan Petroleum', 'GAIL.NS': 'GAIL India',
            'PETRONET.NS': 'Petronet LNG', 'OIL.NS': 'Oil India', 'MGL.NS': 'Mahanagar Gas', 'IGL.NS': 'Indraprastha Gas',

            # Metals & Mining
            'TATASTEEL.NS': 'Tata Steel', 'JSWSTEEL.NS': 'JSW Steel', 'HINDALCO.NS': 'Hindalco Industries',
            'VEDL.NS': 'Vedanta Limited', 'COALINDIA.NS': 'Coal India', 'SAIL.NS': 'Steel Authority of India',
            'JINDALSTEL.NS': 'Jindal Steel & Power', 'NMDC.NS': 'NMDC Limited', 'NATIONALUM.NS': 'National Aluminium Company',

            # Cement
            'ULTRACEMCO.NS': 'UltraTech Cement', 'GRASIM.NS': 'Grasim Industries', 'SHREECEM.NS': 'Shree Cement',
            'AMBUJACEM.NS': 'Ambuja Cements', 'ACC.NS': 'ACC Limited', 'DALMIACEMT.NS': 'Dalmia Bharat',

            # Telecom
            'BHARTIARTL.NS': 'Bharti Airtel', 'RCOM.NS': 'Reliance Communications', 'IDEA.NS': 'Vodafone Idea',

            # Power & Utilities
            'NTPC.NS': 'NTPC Limited', 'POWERGRID.NS': 'Power Grid Corporation', 'ADANIPOWER.NS': 'Adani Power',
            'TATAPOWER.NS': 'Tata Power', 'NHPC.NS': 'NHPC Limited', 'SJVN.NS': 'SJVN Limited',

            # Infrastructure
            'LT.NS': 'Larsen & Toubro', 'ADANIPORTS.NS': 'Adani Ports', 'ADANIENT.NS': 'Adani Enterprises',
            'GMRINFRA.NS': 'GMR Infrastructure', 'IRB.NS': 'IRB Infrastructure', 'CONCOR.NS': 'Container Corporation of India',

            # Defence & Aerospace
            'HAL.NS': 'Hindustan Aeronautics', 'BEL.NS': 'Bharat Electronics', 'BEML.NS': 'BEML Limited',
            'BHEL.NS': 'Bharat Heavy Electricals', 'GRSE.NS': 'Garden Reach Shipbuilders',

            # Paints & Specialty
            'ASIANPAINT.NS': 'Asian Paints', 'BERGER.NS': 'Berger Paints', 'AKZONOBEL.NS': 'Akzo Nobel India',

            # Jewellery & Luxury
            'TITAN.NS': 'Titan Company', 'RAJESHEXPO.NS': 'Rajesh Exports',

            # Retail & E-commerce
            'TRENT.NS': 'Trent Limited', 'AVENUE.NS': 'Avenue Supermarts', 'SHOPERSTOP.NS': 'Shoppers Stop',
            'RELAXO.NS': 'Relaxo Footwears', 'BATA.NS': 'Bata India',

            # Media & Entertainment
            'ZEEL.NS': 'Zee Entertainment', 'SUNTV.NS': 'Sun TV Network', 'NETWORK18.NS': 'Network18 Media',

            # Real Estate
            'DLF.NS': 'DLF Limited', 'GODREJPROP.NS': 'Godrej Properties', 'OBEROIRLTY.NS': 'Oberoi Realty',
            'BRIGADE.NS': 'Brigade Enterprises', 'PRESTIGE.NS': 'Prestige Estates',

            # Hospitality & Travel
            'INDHOTEL.NS': 'Indian Hotels Company', 'LEMONTREE.NS': 'Lemon Tree Hotels', 'SPICEJET.NS': 'SpiceJet',
            'IRCTC.NS': 'Indian Railway Catering'
        }

    def get_stock_news(self, symbol, days_back=7):
        """Get news articles for a specific stock symbol"""
        news_articles = []

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        try:
            # Try NewsAPI first
            if self.news_api:
                articles = self._get_newsapi_articles(symbol, start_date, end_date)
                news_articles.extend(articles)

            # Fallback to Yahoo Finance news scraping
            yahoo_articles = self._get_yahoo_news(symbol)
            news_articles.extend(yahoo_articles)

        except Exception as e:
            print(f"Error fetching news for {symbol}: {e}")

        return news_articles

    def _get_newsapi_articles(self, symbol, start_date, end_date):
        """Get articles from NewsAPI"""
        articles = []

        try:
            # Get company name for better search
            company_name = self.indian_company_names.get(symbol, symbol.replace('.NS', ''))

            # Search for company name and Indian market terms
            query = f'"{company_name}" OR "{symbol}" OR "NSE" OR "BSE" OR "Indian stock"'

            response = self.news_api.get_everything(
                q=query,
                from_param=start_date.strftime('%Y-%m-%d'),
                to=end_date.strftime('%Y-%m-%d'),
                language='en',
                sort_by='relevancy',
                page_size=20,
                domains='economictimes.com,moneycontrol.com,business-standard.com,livemint.com,financialexpress.com'
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
                        'symbol': symbol
                    })

        except Exception as e:
            print(f"NewsAPI error for {symbol}: {e}")

        return articles

    def _get_yahoo_news(self, symbol):
        """Scrape news from Yahoo Finance as fallback"""
        articles = []

        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            news = ticker.news

            for item in news[:10]:  # Limit to 10 articles
                articles.append({
                    'title': item.get('title', ''),
                    'description': item.get('summary', ''),
                    'content': item.get('summary', ''),
                    'url': item.get('link', ''),
                    'published_at': datetime.fromtimestamp(item.get('providerPublishTime', 0)).isoformat(),
                    'source': item.get('publisher', 'Yahoo Finance'),
                    'symbol': symbol
                })

        except Exception as e:
            print(f"Yahoo Finance news error for {symbol}: {e}")

        return articles

    def get_market_news(self):
        """Get general Indian market news"""
        articles = []

        try:
            if self.news_api:
                # Get Indian market news
                response = self.news_api.get_everything(
                    q='NSE OR BSE OR "Indian stock market" OR "Sensex" OR "Nifty" OR "Indian economy"',
                    language='en',
                    sort_by='publishedAt',
                    page_size=20,
                    domains='economictimes.com,moneycontrol.com,business-standard.com,livemint.com,financialexpress.com'
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
                            'symbol': 'MARKET'
                        })

        except Exception as e:
            print(f"Market news error: {e}")

        return articles

    def collect_all_news(self, symbols):
        """Collect news for all symbols"""
        all_news = []

        print("Collecting market news...")
        market_news = self.get_market_news()
        all_news.extend(market_news)

        print(f"Collecting news for {len(symbols)} stocks...")
        for i, symbol in enumerate(symbols):
            print(f"Processing {symbol} ({i+1}/{len(symbols)})")
            stock_news = self.get_stock_news(symbol, Config.NEWS_LOOKBACK_DAYS)
            all_news.extend(stock_news)

            # Rate limiting
            time.sleep(0.1)

        return pd.DataFrame(all_news)
