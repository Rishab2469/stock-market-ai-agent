import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import Config

class StockDataCollector:
    def __init__(self):
        self.cache = {}

    def get_stock_data(self, symbol, period='1mo'):
        """Get stock price data and metrics"""
        try:
            ticker = yf.Ticker(symbol)

            # Get historical data
            hist = ticker.history(period=period)
            if hist.empty:
                return None

            # Get stock info
            info = ticker.info

            # Calculate metrics
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            price_change = (current_price - prev_close) / prev_close

            # Volume analysis
            avg_volume = hist['Volume'].tail(20).mean()
            current_volume = hist['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1

            # Volatility (20-day)
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.tail(20).std() * np.sqrt(252)  # Annualized

            # Moving averages (Simple)
            ma_20 = hist['Close'].tail(min(20, len(hist))).mean() if len(hist) >= 5 else current_price
            ma_50 = hist['Close'].tail(min(50, len(hist))).mean() if len(hist) >= 10 else ma_20
            ma_200 = hist['Close'].tail(min(200, len(hist))).mean() if len(hist) >= 50 else ma_50

            # Exponential Moving Averages (EMA)
            ema_20 = self._calculate_ema(hist['Close'], 20)
            ema_50 = self._calculate_ema(hist['Close'], 50)
            ema_200 = self._calculate_ema(hist['Close'], 200)

            # Technical Indicators
            rsi = self._calculate_rsi(hist['Close'])
            macd_line, macd_signal, macd_histogram = self._calculate_macd(hist['Close'])
            bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(hist['Close'])
            stoch_k, stoch_d = self._calculate_stochastic(hist)

            # Clean and validate all numeric values to prevent NaN
            def safe_float(value, default=0.0):
                """Safely convert to float, handling NaN and None"""
                try:
                    if pd.isna(value) or value is None:
                        return default
                    return float(value)
                except (ValueError, TypeError):
                    return default

            # Get additional financial metrics
            dividend_yield = safe_float(info.get('dividendYield'), 0.0) * 100 if info.get('dividendYield') else 0.0
            book_value = safe_float(info.get('bookValue'), None)
            pb_ratio = safe_float(info.get('priceToBook'), None)
            roe = safe_float(info.get('returnOnEquity'), None)
            debt_to_equity = safe_float(info.get('debtToEquity'), None)
            current_ratio = safe_float(info.get('currentRatio'), None)

            stock_data = {
                'symbol': symbol,
                'current_price': safe_float(current_price, 0.0),
                'price_change': safe_float(price_change, 0.0),
                'volume_ratio': safe_float(volume_ratio, 1.0),
                'volatility': safe_float(volatility, 0.0),
                'market_cap': safe_float(info.get('marketCap', 0), 0),

                # Valuation Metrics
                'pe_ratio': safe_float(info.get('trailingPE'), None),
                'pb_ratio': pb_ratio,
                'book_value': book_value,
                'beta': safe_float(info.get('beta'), None),

                # Moving Averages
                'ma_20': safe_float(ma_20, current_price),
                'ma_50': safe_float(ma_50, current_price),
                'ma_200': safe_float(ma_200, current_price),

                # Exponential Moving Averages
                'ema_20': safe_float(ema_20, current_price),
                'ema_50': safe_float(ema_50, current_price),
                'ema_200': safe_float(ema_200, current_price),

                # Technical Indicators
                'rsi': safe_float(rsi, 50.0),
                'macd_line': safe_float(macd_line, 0.0),
                'macd_signal': safe_float(macd_signal, 0.0),
                'macd_histogram': safe_float(macd_histogram, 0.0),
                'bb_upper': safe_float(bb_upper, current_price),
                'bb_middle': safe_float(bb_middle, current_price),
                'bb_lower': safe_float(bb_lower, current_price),
                'stoch_k': safe_float(stoch_k, 50.0),
                'stoch_d': safe_float(stoch_d, 50.0),

                # Financial Health
                'dividend_yield': dividend_yield,
                'roe': roe,
                'debt_to_equity': debt_to_equity,
                'current_ratio': current_ratio,

                # Company Info
                'sector': str(info.get('sector', 'Unknown')),
                'industry': str(info.get('industry', 'Unknown')),
                'recommendation': str(info.get('recommendationKey', 'none')),
                'target_price': safe_float(info.get('targetMeanPrice'), None),
                'analyst_count': safe_float(info.get('numberOfAnalystOpinions', 0), 0),
                'last_updated': datetime.now().isoformat()
            }

            return stock_data

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1] if not rsi.empty else 50
        except:
            return 50

    def _calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        try:
            if len(prices) < period:
                return prices.mean()
            ema = prices.ewm(span=period, adjust=False).mean()
            return ema.iloc[-1] if not ema.empty else prices.iloc[-1]
        except:
            return prices.iloc[-1] if not prices.empty else 0

    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            if len(prices) < slow:
                return 0, 0, 0

            ema_fast = prices.ewm(span=fast).mean()
            ema_slow = prices.ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            macd_signal = macd_line.ewm(span=signal).mean()
            macd_histogram = macd_line - macd_signal

            return (
                macd_line.iloc[-1] if not macd_line.empty else 0,
                macd_signal.iloc[-1] if not macd_signal.empty else 0,
                macd_histogram.iloc[-1] if not macd_histogram.empty else 0
            )
        except:
            return 0, 0, 0

    def _calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        try:
            if len(prices) < period:
                current_price = prices.iloc[-1]
                return current_price, current_price, current_price

            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()

            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)

            return (
                upper_band.iloc[-1] if not upper_band.empty else prices.iloc[-1],
                sma.iloc[-1] if not sma.empty else prices.iloc[-1],
                lower_band.iloc[-1] if not lower_band.empty else prices.iloc[-1]
            )
        except:
            current_price = prices.iloc[-1] if not prices.empty else 0
            return current_price, current_price, current_price

    def _calculate_stochastic(self, hist, k_period=14, d_period=3):
        """Calculate Stochastic Oscillator"""
        try:
            if len(hist) < k_period:
                return 50, 50

            high = hist['High']
            low = hist['Low']
            close = hist['Close']

            lowest_low = low.rolling(window=k_period).min()
            highest_high = high.rolling(window=k_period).max()

            k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            d_percent = k_percent.rolling(window=d_period).mean()

            return (
                k_percent.iloc[-1] if not k_percent.empty else 50,
                d_percent.iloc[-1] if not d_percent.empty else 50
            )
        except:
            return 50, 50

    def get_multiple_stocks(self, symbols):
        """Get data for multiple stocks"""
        stock_data = []

        print(f"Fetching data for {len(symbols)} stocks...")
        for i, symbol in enumerate(symbols):
            print(f"Processing {symbol} ({i+1}/{len(symbols)})")
            data = self.get_stock_data(symbol)
            if data:
                stock_data.append(data)

        return pd.DataFrame(stock_data)

    def get_market_overview(self):
        """Get overall Indian market indicators"""
        try:
            # Major Indian indices
            indices = {
                '^NSEI': 'Nifty 50',
                '^BSESN': 'Sensex',
                '^NSEBANK': 'Bank Nifty',
                '^NSEIT': 'Nifty IT'
            }

            market_data = {}
            for symbol, name in indices.items():
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='5d')
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
                    change = (current - prev) / prev

                    market_data[symbol] = {
                        'name': name,
                        'price': current,
                        'change': change
                    }

            return market_data

        except Exception as e:
            print(f"Error fetching market overview: {e}")
            return {}

    def screen_stocks(self, df):
        """Apply basic screening criteria with NaN handling"""
        if df.empty:
            return df

        try:
            # Clean data first - replace NaN with defaults
            df = df.fillna({
                'market_cap': 0,
                'volume_ratio': 1.0,
                'price_change': 0.0,
                'rsi': 50.0,
                'current_price': 0.0,
                'volatility': 0.0
            })

            # Filter by market cap (keep stocks with valid market cap)
            df = df[df['market_cap'] >= Config.MIN_MARKET_CAP]

            # Filter by volume (active stocks)
            df = df[df['volume_ratio'] >= 0.5]

            # Filter out extreme price movements (potential manipulation)
            df = df[abs(df['price_change']) <= Config.MAX_PRICE_CHANGE]

            # Filter by RSI (not overbought)
            df = df[df['rsi'] <= 80]

            # Filter out stocks with zero price (invalid data)
            df = df[df['current_price'] > 0]

            print(f"Screening complete: {len(df)} stocks passed filters")
            return df

        except Exception as e:
            print(f"Error in screening: {e}")
            return df
