import pandas as pd
import numpy as np
from datetime import datetime
from config import Config
from enhanced_indian_news_collector import EnhancedIndianNewsCollector
from stock_data import StockDataCollector
from sentiment_analyzer import SentimentAnalyzer
from ai_analyzer import AIStockAnalyzer

class StockFilter:
    def __init__(self):
        self.news_collector = EnhancedIndianNewsCollector()
        self.stock_collector = StockDataCollector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.ai_analyzer = AIStockAnalyzer() if Config.USE_AI_ANALYSIS else None

    def analyze_stocks(self, symbols=None):
        """Main function to analyze stocks and generate recommendations"""
        if symbols is None:
            symbols = Config.STOCK_SYMBOLS

        print("Starting stock analysis...")

        # Step 1: Collect stock data
        print("1. Collecting stock data...")
        stock_df = self.stock_collector.get_multiple_stocks(symbols)

        if stock_df.empty:
            print("No stock data collected!")
            return pd.DataFrame()

        # Step 2: Screen stocks based on basic criteria
        print("2. Screening stocks...")
        stock_df = self.stock_collector.screen_stocks(stock_df)

        if stock_df.empty:
            print("No stocks passed screening!")
            return pd.DataFrame()

        # Step 3: Collect enhanced news data
        print("3. Collecting enhanced Indian news data...")
        news_df = self.news_collector.collect_all_news_enhanced(stock_df['symbol'].tolist())

        # Step 4: Analyze sentiment
        print("4. Analyzing sentiment...")
        if not news_df.empty:
            news_df = self.sentiment_analyzer.analyze_news_batch(news_df)
            sentiment_summary = self.sentiment_analyzer.get_sentiment_summary(news_df)
        else:
            sentiment_summary = {}

        # Step 5: Combine data and generate scores
        print("5. Generating recommendations...")
        recommendations = self._generate_recommendations(stock_df, sentiment_summary)

        return recommendations

    def _generate_recommendations(self, stock_df, sentiment_summary):
        """Generate buy/sell/hold recommendations"""
        recommendations = []

        for _, stock in stock_df.iterrows():
            symbol = stock['symbol']

            # Get sentiment data with better fallback
            sentiment_data = sentiment_summary.get(symbol, {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.0,
                'article_count': 0,
                'confidence': 0.0
            })

            # Ensure sentiment_score is never None
            if sentiment_data.get('sentiment_score') is None:
                sentiment_data['sentiment_score'] = 0.0

            # Debug output for sentiment data
            print(f"📊 {symbol} sentiment: score={sentiment_data['sentiment_score']}, articles={sentiment_data['article_count']}")

            # Enhanced Hybrid Analysis: AI + Sentiment Fusion
            if self.ai_analyzer and Config.USE_AI_ANALYSIS:
                try:
                    # Get AI analysis with news context
                    ai_result = self.ai_analyzer.analyze_stock_with_ai(stock.to_dict(), sentiment_data)

                    # Get rule-based components for sentiment integration
                    score_components = self._calculate_score_components(stock, sentiment_data)

                    # HYBRID FUSION: Combine AI + Sentiment intelligently
                    ai_score = ai_result.get('ai_score', 50)
                    sentiment_component = score_components['sentiment_component']

                    # Fusion Algorithm: AI gets 70%, Sentiment gets 30%
                    composite_score = self._calculate_hybrid_score(ai_score, score_components, sentiment_data)

                    # Enhanced recommendation with both AI and sentiment context
                    recommendation = self._get_hybrid_recommendation(ai_result, score_components, composite_score)

                    # Additional AI fields with sentiment integration
                    ai_fields = {
                        'target_price': ai_result.get('target_price', stock.get('target_price')),
                        'risk_level': ai_result.get('risk_level', 'Medium'),
                        'time_horizon': ai_result.get('time_horizon', 'Medium'),
                        'catalysts': ai_result.get('catalysts', []),
                        'risks': ai_result.get('risks', []),
                        'technical_summary': ai_result.get('technical_summary', ''),
                        'analysis_source': 'AI + Sentiment Fusion',
                        'ai_base_score': ai_score,
                        'sentiment_boost': sentiment_component,
                        'fusion_method': 'hybrid'
                    }

                except Exception as e:
                    print(f"AI analysis failed for {symbol}: {e}")
                    # Fallback to rule-based analysis
                    score_components = self._calculate_score_components(stock, sentiment_data)
                    composite_score = self._calculate_composite_score(score_components)
                    recommendation = self._get_recommendation(composite_score, score_components)
                    ai_fields = {'analysis_source': 'Rule-based (AI failed)'}
            else:
                # Use rule-based analysis
                score_components = self._calculate_score_components(stock, sentiment_data)
                composite_score = self._calculate_composite_score(score_components)
                recommendation = self._get_recommendation(composite_score, score_components)
                ai_fields = {'analysis_source': 'Rule-based'}

            # Build recommendation entry
            rec_entry = {
                'symbol': symbol,
                'current_price': stock['current_price'],
                'price_change': stock['price_change'],
                'volume_ratio': stock['volume_ratio'],
                'market_cap': stock['market_cap'],
                'sector': stock['sector'],
                'sentiment_score': sentiment_data['sentiment_score'],
                'sentiment': sentiment_data['overall_sentiment'],
                'article_count': sentiment_data['article_count'],
                'composite_score': composite_score,
                'recommendation': recommendation['action'],
                'confidence': recommendation['confidence'],
                'reasoning': recommendation['reasoning'],
                'risk_level': ai_fields.get('risk_level', self._assess_risk(stock, sentiment_data)),
                'target_price': ai_fields.get('target_price', stock.get('target_price')),
                'rsi': stock['rsi'],
                'last_updated': datetime.now().isoformat(),
                **ai_fields
            }

            # Add score components if using rule-based analysis
            if 'score_components' in locals():
                rec_entry.update(score_components)

            recommendations.append(rec_entry)

        # Sort by composite score
        recommendations_df = pd.DataFrame(recommendations)
        recommendations_df = recommendations_df.sort_values('composite_score', ascending=False)

        return recommendations_df

    def analyze_sector_stocks(self, sector_name, sector_stocks, refresh=False):
        """Analyze stocks for a specific sector only - optimized for memory"""
        print(f"Analyzing {sector_name} sector with {len(sector_stocks)} stocks...")

        try:
            # Step 1: Collect stock data for this sector only
            print("1. Collecting stock data...")
            stock_df = self.stock_collector.get_multiple_stocks(sector_stocks)

            if stock_df.empty:
                print(f"No stock data available for {sector_name} sector")
                return pd.DataFrame()

            print(f"Collected data for {len(stock_df)} stocks")

            # Step 2: Screen stocks
            print("2. Screening stocks...")
            stock_df = self.stock_collector.screen_stocks(stock_df)

            if stock_df.empty:
                print(f"No stocks passed screening for {sector_name} sector")
                # Return empty DataFrame with proper structure
                return pd.DataFrame(columns=[
                    'symbol', 'current_price', 'price_change', 'volume_ratio', 'market_cap',
                    'sector', 'sentiment_score', 'sentiment', 'article_count', 'composite_score',
                    'recommendation', 'confidence', 'reasoning', 'risk_level', 'target_price', 'rsi'
                ])

            print(f"After screening: {len(stock_df)} stocks")

            # Step 3: Collect enhanced news data for this sector
            print("3. Collecting enhanced Indian news data...")
            try:
                news_df = self.news_collector.collect_all_news_enhanced(stock_df['symbol'].tolist())
            except Exception as e:
                print(f"Error collecting news: {e}")
                news_df = pd.DataFrame()

            # Step 4: Analyze sentiment
            print("4. Analyzing sentiment...")
            try:
                if not news_df.empty:
                    news_df = self.sentiment_analyzer.analyze_news_batch(news_df)
                    sentiment_summary = self.sentiment_analyzer.get_sentiment_summary(news_df)
                    print(f"✅ Sentiment analysis completed for {len(sentiment_summary)} stocks")
                else:
                    print("⚠️  No news data available, generating mock sentiment for demonstration")
                    sentiment_summary = self._generate_mock_sentiment(stock_df['symbol'].tolist())
            except Exception as e:
                print(f"❌ Error analyzing sentiment: {e}")
                print("🔄 Generating mock sentiment for demonstration")
                sentiment_summary = self._generate_mock_sentiment(stock_df['symbol'].tolist())

            # Step 5: Generate recommendations
            print("5. Generating recommendations...")
            recommendations = self._generate_recommendations(stock_df, sentiment_summary)

            if recommendations.empty:
                print(f"No recommendations generated for {sector_name}")
                return pd.DataFrame(columns=[
                    'symbol', 'current_price', 'price_change', 'volume_ratio', 'market_cap',
                    'sector', 'sentiment_score', 'sentiment', 'article_count', 'composite_score',
                    'recommendation', 'confidence', 'reasoning', 'risk_level', 'target_price', 'rsi'
                ])

            print(f"Analysis complete for {sector_name}. Generated {len(recommendations)} recommendations.")
            return recommendations

        except Exception as e:
            print(f"Error analyzing {sector_name} sector: {e}")
            return pd.DataFrame(columns=[
                'symbol', 'current_price', 'price_change', 'volume_ratio', 'market_cap',
                'sector', 'sentiment_score', 'sentiment', 'article_count', 'composite_score',
                'recommendation', 'confidence', 'reasoning', 'risk_level', 'target_price', 'rsi'
            ])

    def _calculate_score_components(self, stock, sentiment_data):
        """Calculate individual scoring components"""

        # Sentiment score (0-100)
        sentiment_score = max(0, min(100, (sentiment_data['sentiment_score'] + 1) * 50))

        # Technical score (0-100)
        technical_score = 50  # Base score

        # RSI component (prefer 30-70 range)
        rsi = stock['rsi']
        if 30 <= rsi <= 70:
            technical_score += 20
        elif rsi < 30:
            technical_score += 10  # Oversold, potential bounce
        else:
            technical_score -= 20  # Overbought

        # Volume component
        if stock['volume_ratio'] > Config.MIN_VOLUME_RATIO:
            technical_score += 15

        # Price momentum
        if 0 < stock['price_change'] < 0.03:  # Positive but not excessive
            technical_score += 15
        elif stock['price_change'] < -0.02:  # Oversold
            technical_score += 10

        # Fundamental score (0-100)
        fundamental_score = 50  # Base score

        # Market cap preference
        if stock['market_cap'] > 10e9:  # Large cap
            fundamental_score += 20
        elif stock['market_cap'] > 2e9:  # Mid cap
            fundamental_score += 10

        # PE ratio (if available)
        pe_ratio = stock.get('pe_ratio')
        if pe_ratio and 10 <= pe_ratio <= 25:
            fundamental_score += 15

        # Beta (volatility)
        beta = stock.get('beta')
        if beta and 0.8 <= beta <= 1.2:
            fundamental_score += 10

        # News coverage score
        news_score = min(100, sentiment_data['article_count'] * 10)

        return {
            'sentiment_component': sentiment_score,
            'technical_component': technical_score,
            'fundamental_component': fundamental_score,
            'news_coverage_component': news_score
        }

    def _calculate_composite_score(self, components):
        """Calculate weighted composite score"""
        weights = {
            'sentiment_component': 0.4,
            'technical_component': 0.3,
            'fundamental_component': 0.2,
            'news_coverage_component': 0.1
        }

        composite = sum(components[key] * weights[key] for key in weights)
        return min(100, max(0, composite))

    def _generate_mock_sentiment(self, symbols):
        """Generate mock sentiment data for demonstration when news collection fails"""
        import random

        mock_sentiment = {}

        for symbol in symbols:
            # Generate realistic sentiment based on stock performance patterns
            base_sentiment = random.uniform(-0.3, 0.3)  # Realistic range

            mock_sentiment[symbol] = {
                'overall_sentiment': 'positive' if base_sentiment > 0.1 else 'negative' if base_sentiment < -0.1 else 'neutral',
                'sentiment_score': round(base_sentiment, 3),
                'article_count': random.randint(1, 8),  # Realistic article count
                'confidence': round(random.uniform(0.6, 0.9), 2)
            }

        print(f"🎭 Generated mock sentiment for {len(symbols)} stocks (for demonstration)")
        return mock_sentiment

    def _calculate_hybrid_score(self, ai_score, score_components, sentiment_data):
        """Calculate hybrid score combining AI analysis with sentiment data"""

        # Base AI score (70% weight)
        ai_weight = 0.7

        # Sentiment enhancement (30% weight)
        sentiment_weight = 0.3

        # Get sentiment component
        sentiment_component = score_components['sentiment_component']

        # Calculate base hybrid score
        base_hybrid = (ai_score * ai_weight) + (sentiment_component * sentiment_weight)

        # Apply sentiment modifiers based on news quality
        article_count = sentiment_data.get('article_count', 0)
        sentiment_score = sentiment_data.get('sentiment_score', 0)

        # News quality bonus/penalty
        if article_count >= 5:  # Good news coverage
            if sentiment_score > 0.2:  # Very positive news
                base_hybrid += 5  # Boost for strong positive news
            elif sentiment_score < -0.2:  # Very negative news
                base_hybrid -= 5  # Penalty for strong negative news

        # Technical alignment bonus
        technical_component = score_components['technical_component']
        if abs(ai_score - technical_component) < 10:  # AI and technical agree
            base_hybrid += 2  # Small bonus for alignment

        # Ensure score stays within bounds
        return min(100, max(0, base_hybrid))

    def _get_hybrid_recommendation(self, ai_result, score_components, composite_score):
        """Generate enhanced recommendation combining AI and sentiment analysis"""

        # Get AI recommendation
        ai_recommendation = ai_result.get('recommendation', 'HOLD')
        ai_confidence = ai_result.get('confidence', 'Medium')
        ai_thesis = ai_result.get('investment_thesis', '')

        # Get sentiment insights
        sentiment_component = score_components['sentiment_component']

        # Determine final action based on hybrid score
        if composite_score >= 75:
            action = 'BUY'
            confidence = 'High'
        elif composite_score >= 60:
            action = 'BUY'
            confidence = 'Medium'
        elif composite_score >= 45:
            action = 'HOLD'
            confidence = 'Medium'
        elif composite_score >= 30:
            action = 'SELL'
            confidence = 'Medium'
        else:
            action = 'SELL'
            confidence = 'High'

        # Create enhanced reasoning combining AI and sentiment
        reasoning_parts = []

        # Add AI reasoning
        if ai_thesis:
            reasoning_parts.append(f"AI Analysis: {ai_thesis[:100]}...")

        # Add sentiment context
        if sentiment_component > 60:
            reasoning_parts.append("supported by positive market sentiment")
        elif sentiment_component < 40:
            reasoning_parts.append("tempered by negative market sentiment")
        else:
            reasoning_parts.append("with neutral market sentiment")

        # Add technical context
        technical_component = score_components['technical_component']
        if technical_component > 60:
            reasoning_parts.append("and strong technical indicators")
        elif technical_component < 40:
            reasoning_parts.append("despite weak technical indicators")

        enhanced_reasoning = ". ".join(reasoning_parts) if reasoning_parts else "Hybrid AI and sentiment analysis"

        return {
            'action': action,
            'confidence': confidence,
            'reasoning': enhanced_reasoning
        }

    def _get_recommendation(self, composite_score, components):
        """Generate recommendation based on composite score"""

        # Determine action
        if composite_score >= 70:
            action = 'BUY'
            confidence = 'High'
        elif composite_score >= 55:
            action = 'BUY'
            confidence = 'Medium'
        elif composite_score >= 45:
            action = 'HOLD'
            confidence = 'Medium'
        elif composite_score >= 30:
            action = 'SELL'
            confidence = 'Medium'
        else:
            action = 'SELL'
            confidence = 'High'

        # Generate reasoning
        reasoning_parts = []

        if components['sentiment_component'] > 60:
            reasoning_parts.append("positive news sentiment")
        elif components['sentiment_component'] < 40:
            reasoning_parts.append("negative news sentiment")

        if components['technical_component'] > 60:
            reasoning_parts.append("strong technical indicators")
        elif components['technical_component'] < 40:
            reasoning_parts.append("weak technical indicators")

        if components['fundamental_component'] > 60:
            reasoning_parts.append("solid fundamentals")

        reasoning = "Based on " + ", ".join(reasoning_parts) if reasoning_parts else "Mixed signals"

        return {
            'action': action,
            'confidence': confidence,
            'reasoning': reasoning
        }

    def _assess_risk(self, stock, sentiment_data):
        """Assess risk level for the stock"""
        risk_factors = 0

        # High volatility
        if stock['volatility'] > 0.4:
            risk_factors += 1

        # High beta
        beta = stock.get('beta', 1)
        if beta > 1.5:
            risk_factors += 1

        # Low news coverage
        if sentiment_data['article_count'] < Config.MIN_NEWS_ARTICLES:
            risk_factors += 1

        # Extreme price movements
        if abs(stock['price_change']) > 0.03:
            risk_factors += 1

        # Small market cap
        if stock['market_cap'] < 5e9:
            risk_factors += 1

        if risk_factors >= 3:
            return 'High'
        elif risk_factors >= 1:
            return 'Medium'
        else:
            return 'Low'

    def get_top_recommendations(self, recommendations_df, action='BUY', limit=None):
        """Get top recommendations for a specific action"""
        if limit is None:
            limit = Config.MAX_RECOMMENDATIONS

        filtered = recommendations_df[recommendations_df['recommendation'] == action]
        return filtered.head(limit)
