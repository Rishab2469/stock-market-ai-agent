import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from datetime import datetime
from config import Config

# Try to import transformers, but don't fail if it's not available
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

class SentimentAnalyzer:
    def __init__(self):
        self.use_transformers = False
        self.sentiment_pipeline = None

        if TRANSFORMERS_AVAILABLE:
            try:
                # Try to load a financial sentiment model
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model="ProsusAI/finbert",
                    tokenizer="ProsusAI/finbert"
                )
                self.use_transformers = True
                print("✓ Using FinBERT for sentiment analysis")
            except:
                try:
                    # Fallback to general sentiment model
                    self.sentiment_pipeline = pipeline("sentiment-analysis")
                    self.use_transformers = True
                    print("✓ Using general transformer model for sentiment analysis")
                except:
                    print("⚠ Could not load transformer models, using TextBlob only")
        else:
            print("⚠ Transformers not installed, using TextBlob for sentiment analysis")

    def analyze_text(self, text):
        """Analyze sentiment of a single text"""
        if not text or pd.isna(text):
            return {'sentiment': 'neutral', 'score': 0.0, 'confidence': 0.0}

        # Clean text
        text = self._clean_text(text)

        # Use transformer model if available
        if self.use_transformers and self.sentiment_pipeline:
            try:
                result = self.sentiment_pipeline(text[:512])  # Limit text length
                sentiment = result[0]['label'].lower()
                confidence = result[0]['score']

                # Convert to standardized format
                if sentiment in ['positive', 'pos']:
                    score = confidence
                elif sentiment in ['negative', 'neg']:
                    score = -confidence
                else:
                    score = 0.0

                return {
                    'sentiment': sentiment,
                    'score': score,
                    'confidence': confidence
                }
            except Exception as e:
                print(f"Transformer analysis failed: {e}")

        # Fallback to TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return {
            'sentiment': sentiment,
            'score': polarity,
            'confidence': abs(polarity)
        }

    def _clean_text(self, text):
        """Clean and preprocess text"""
        if not text:
            return ""

        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\!\?\,\-]', '', text)

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text

    def analyze_news_batch(self, news_df):
        """Analyze sentiment for a batch of news articles"""
        if news_df.empty:
            return news_df

        results = []

        print(f"Analyzing sentiment for {len(news_df)} articles...")

        for idx, row in news_df.iterrows():
            # Combine title and description for analysis
            text = f"{row.get('title', '')} {row.get('description', '')}"

            sentiment_result = self.analyze_text(text)

            results.append({
                'index': idx,
                'sentiment': sentiment_result['sentiment'],
                'sentiment_score': sentiment_result['score'],
                'confidence': sentiment_result['confidence']
            })

        # Merge results back to dataframe
        sentiment_df = pd.DataFrame(results).set_index('index')
        news_df = news_df.join(sentiment_df)

        return news_df

    def calculate_stock_sentiment(self, news_df, symbol):
        """Calculate overall sentiment score for a specific stock"""
        if news_df.empty:
            return {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.0,
                'article_count': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0
            }

        # Filter news for this symbol
        stock_news = news_df[news_df['symbol'] == symbol].copy()

        if stock_news.empty:
            return {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.0,
                'article_count': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0
            }

        # Count sentiment categories
        sentiment_counts = stock_news['sentiment'].value_counts()
        positive_count = sentiment_counts.get('positive', 0)
        negative_count = sentiment_counts.get('negative', 0)
        neutral_count = sentiment_counts.get('neutral', 0)

        # Calculate weighted sentiment score
        # Weight recent articles more heavily
        stock_news['published_at'] = pd.to_datetime(stock_news['published_at'])
        stock_news = stock_news.sort_values('published_at', ascending=False)

        # Apply time decay weights (more recent = higher weight)
        weights = np.exp(-np.arange(len(stock_news)) * 0.1)
        weighted_scores = stock_news['sentiment_score'] * weights
        overall_score = weighted_scores.sum() / weights.sum() if len(weights) > 0 else 0

        # Determine overall sentiment
        if overall_score > 0.1:
            overall_sentiment = 'positive'
        elif overall_score < -0.1:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'

        return {
            'overall_sentiment': overall_sentiment,
            'sentiment_score': overall_score,
            'article_count': len(stock_news),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'confidence': stock_news['confidence'].mean() if len(stock_news) > 0 else 0
        }

    def get_sentiment_summary(self, news_df):
        """Get sentiment summary for all stocks"""
        symbols = news_df['symbol'].unique()
        sentiment_summary = {}

        for symbol in symbols:
            if symbol != 'MARKET':  # Skip general market news
                sentiment_summary[symbol] = self.calculate_stock_sentiment(news_df, symbol)

        return sentiment_summary
