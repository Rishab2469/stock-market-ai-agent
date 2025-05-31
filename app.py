from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
from datetime import datetime
from config import Config
from stock_filter import StockFilter
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)
app.config.from_object(Config)

# Global variables to cache data
cached_recommendations = None
last_update = None
stock_filter = StockFilter()  # Initialize the stock filter globally

def get_recommendations(force_refresh=False):
    """Get recommendations with caching"""
    global cached_recommendations, last_update, stock_filter

    # Check if we need to refresh (cache for 30 minutes)
    if (force_refresh or
        cached_recommendations is None or
        last_update is None or
        (datetime.now() - last_update).seconds > 1800):

        print("Refreshing recommendations...")
        cached_recommendations = stock_filter.analyze_stocks()
        last_update = datetime.now()

    return cached_recommendations

@app.route('/')
def index():
    """Main dashboard page - sector-first approach"""
    return render_template('sector_analysis.html')

@app.route('/old')
def old_index():
    """Old dashboard page"""
    return render_template('index.html')

@app.route('/api/recommendations')
def api_recommendations():
    """API endpoint for sector-specific recommendations"""
    global last_update, stock_filter

    try:
        # Get sector parameter (required)
        sector = request.args.get('sector', '').upper()
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'

        if not sector:
            return jsonify({
                'status': 'error',
                'message': 'Sector parameter is required. Use /api/sectors to get available sectors.',
                'data': []
            })

        # Validate sector
        from config import Config
        if sector not in Config.STOCK_SECTORS:
            return jsonify({
                'status': 'error',
                'message': f'Invalid sector: {sector}. Use /api/sectors to get available sectors.',
                'data': []
            })

        print(f"Analyzing {sector} sector...")

        # Get stocks for the specific sector
        sector_stocks = Config.STOCK_SECTORS[sector]

        # Run analysis only for this sector's stocks
        recommendations = stock_filter.analyze_sector_stocks(sector, sector_stocks, force_refresh)
        last_update = datetime.now()

        if recommendations is None or recommendations.empty:
            return jsonify({
                'status': 'error',
                'message': f'No data available for {sector} sector',
                'data': []
            })

        # Clean DataFrame first to remove any NaN values
        recommendations = recommendations.fillna({
            'current_price': 0.0,
            'price_change': 0.0,
            'sentiment_score': 0.0,
            'composite_score': 0.0,
            'market_cap': 0.0,
            'volume_ratio': 1.0,
            'rsi': 50.0,
            'recommendation': 'HOLD',
            'confidence': 'Low',
            'sentiment': 'neutral',
            'sector': 'Unknown',
            'symbol': '',
            'reasoning': 'No analysis available',
            'risk_level': 'Medium',
            'target_price': 0.0,
            'article_count': 0
        })

        # Convert to JSON-serializable format
        data = recommendations.to_dict('records')

        # Format numbers for display (Indian format) with comprehensive NaN handling
        cleaned_data = []
        for item in data:
            try:
                # Create a clean item with safe conversions
                clean_item = {}

                # Handle numeric fields with multiple fallbacks
                def safe_number(value, default=0.0):
                    try:
                        if pd.isna(value) or value is None or str(value).lower() in ['nan', 'none', '']:
                            return default
                        return float(value)
                    except (ValueError, TypeError, AttributeError):
                        return default

                # Safe string conversion
                def safe_string(value, default=''):
                    try:
                        if pd.isna(value) or value is None:
                            return default
                        return str(value)
                    except (ValueError, TypeError, AttributeError):
                        return default

                # Process all fields safely
                clean_item['current_price'] = round(safe_number(item.get('current_price', 0)), 2)
                clean_item['price_change'] = round(safe_number(item.get('price_change', 0)) * 100, 2)
                clean_item['sentiment_score'] = round(safe_number(item.get('sentiment_score', 0)), 3)
                clean_item['composite_score'] = round(safe_number(item.get('composite_score', 0)), 1)
                clean_item['volume_ratio'] = round(safe_number(item.get('volume_ratio', 1)), 2)
                clean_item['rsi'] = round(safe_number(item.get('rsi', 50)), 1)
                clean_item['target_price'] = round(safe_number(item.get('target_price', 0)), 2)
                clean_item['article_count'] = int(safe_number(item.get('article_count', 0)))

                # Additional technical indicators
                clean_item['pe_ratio'] = round(safe_number(item.get('pe_ratio', 0)), 2) if safe_number(item.get('pe_ratio', 0)) > 0 else None
                clean_item['beta'] = round(safe_number(item.get('beta', 0)), 2) if safe_number(item.get('beta', 0)) > 0 else None

                # Moving averages with fallback to current price
                ma_20_val = safe_number(item.get('ma_20', 0))
                ma_50_val = safe_number(item.get('ma_50', 0))
                current_price_val = safe_number(item.get('current_price', 0))

                clean_item['ma_20'] = round(ma_20_val if ma_20_val > 0 else current_price_val, 2)
                clean_item['ma_50'] = round(ma_50_val if ma_50_val > 0 else current_price_val, 2)
                clean_item['volatility'] = round(safe_number(item.get('volatility', 0)), 4)

                # Format market cap safely
                market_cap = safe_number(item.get('market_cap', 0))
                clean_item['market_cap'] = f"₹{market_cap/1e7:.1f}Cr" if market_cap > 0 else "₹0.0Cr"

                # Handle string fields
                clean_item['symbol'] = safe_string(item.get('symbol', ''))
                clean_item['symbol_display'] = clean_item['symbol'].replace('.NS', '')
                clean_item['recommendation'] = safe_string(item.get('recommendation', 'HOLD'))
                clean_item['confidence'] = safe_string(item.get('confidence', 'Low'))
                clean_item['sentiment'] = safe_string(item.get('sentiment', 'neutral'))
                clean_item['sector'] = safe_string(item.get('sector', 'Unknown'))
                clean_item['reasoning'] = safe_string(item.get('reasoning', 'No analysis available'))
                clean_item['risk_level'] = safe_string(item.get('risk_level', 'Medium'))

                cleaned_data.append(clean_item)

            except Exception as e:
                print(f"Error processing item {item.get('symbol', 'unknown')}: {e}")
                # Skip this item rather than crash
                continue

        data = cleaned_data

        return jsonify({
            'status': 'success',
            'data': data,
            'sector': sector,
            'sector_display': sector.replace('_', ' ').title(),
            'last_updated': last_update.isoformat() if last_update else None,
            'total_count': len(data)
        })

    except Exception as e:
        print(f"Error in sector recommendations: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': []
        })

@app.route('/api/recommendations/<action>')
def api_recommendations_by_action(action):
    """Get recommendations filtered by action (BUY/SELL/HOLD)"""
    try:
        recommendations = get_recommendations()

        if recommendations.empty:
            return jsonify({'status': 'error', 'message': 'No data available'})

        filtered = recommendations[recommendations['recommendation'] == action.upper()]
        data = filtered.to_dict('records')

        # Format numbers (Indian format)
        for item in data:
            item['current_price'] = round(item['current_price'], 2)
            item['price_change'] = round(item['price_change'] * 100, 2)
            item['sentiment_score'] = round(item['sentiment_score'], 3)
            item['composite_score'] = round(item['composite_score'], 1)
            item['market_cap'] = f"₹{item['market_cap']/1e7:.1f}Cr"
            item['symbol_display'] = item['symbol'].replace('.NS', '')

        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/charts/sentiment-distribution')
def api_sentiment_distribution():
    """Get sentiment distribution chart data"""
    try:
        recommendations = get_recommendations()

        if recommendations.empty:
            return jsonify({'status': 'error', 'message': 'No data available'})

        sentiment_counts = recommendations['sentiment'].value_counts()

        fig = go.Figure(data=[
            go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                hole=0.3,
                marker_colors=['#28a745', '#ffc107', '#dc3545']
            )
        ])

        fig.update_layout(
            title="News Sentiment Distribution",
            showlegend=True
        )

        return jsonify({
            'status': 'success',
            'chart': json.loads(fig.to_json())
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/charts/recommendation-distribution')
def api_recommendation_distribution():
    """Get recommendation distribution chart data"""
    try:
        recommendations = get_recommendations()

        if recommendations.empty:
            return jsonify({'status': 'error', 'message': 'No data available'})

        rec_counts = recommendations['recommendation'].value_counts()

        fig = go.Figure(data=[
            go.Bar(
                x=rec_counts.index,
                y=rec_counts.values,
                marker_color=['#28a745', '#ffc107', '#dc3545']
            )
        ])

        fig.update_layout(
            title="Recommendation Distribution",
            xaxis_title="Recommendation",
            yaxis_title="Count"
        )

        return jsonify({
            'status': 'success',
            'chart': json.loads(fig.to_json())
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/recommendations/sector/<sector>')
def api_recommendations_by_sector(sector):
    """Get recommendations filtered by sector"""
    try:
        from config import Config

        # Get sector stocks
        sector_stocks = Config.STOCK_SECTORS.get(sector.upper(), [])
        if not sector_stocks:
            return jsonify({'status': 'error', 'message': f'Sector {sector} not found'})

        recommendations = get_recommendations()
        if recommendations.empty:
            return jsonify({'status': 'error', 'message': 'No data available'})

        # Filter by sector stocks
        filtered = recommendations[recommendations['symbol'].isin(sector_stocks)]
        data = filtered.to_dict('records')

        # Format numbers
        for item in data:
            item['current_price'] = round(item['current_price'], 2)
            item['price_change'] = round(item['price_change'] * 100, 2)
            item['sentiment_score'] = round(item['sentiment_score'], 3)
            item['composite_score'] = round(item['composite_score'], 1)
            item['market_cap'] = f"₹{item['market_cap']/1e7:.1f}Cr"
            item['symbol_display'] = item['symbol'].replace('.NS', '')

        return jsonify({
            'status': 'success',
            'sector': sector.upper(),
            'data': data,
            'count': len(data)
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/sectors')
def api_sectors():
    """Get all available sectors"""
    try:
        from config import Config

        sectors = []
        for sector_name, stocks in Config.STOCK_SECTORS.items():
            sectors.append({
                'name': sector_name,
                'display_name': sector_name.replace('_', ' ').title(),
                'stock_count': len(stocks),
                'stocks': [stock.replace('.NS', '') for stock in stocks[:5]]  # Show first 5 stocks
            })

        return jsonify({
            'status': 'success',
            'sectors': sectors,
            'total_sectors': len(sectors)
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/stats')
def api_stats():
    """Get summary statistics"""
    try:
        from config import Config
        recommendations = get_recommendations()

        if recommendations.empty:
            return jsonify({'status': 'error', 'message': 'No data available'})

        # Basic stats
        stats = {
            'total_stocks': len(recommendations),
            'buy_recommendations': len(recommendations[recommendations['recommendation'] == 'BUY']),
            'sell_recommendations': len(recommendations[recommendations['recommendation'] == 'SELL']),
            'hold_recommendations': len(recommendations[recommendations['recommendation'] == 'HOLD']),
            'avg_sentiment_score': round(recommendations['sentiment_score'].mean(), 3),
            'avg_composite_score': round(recommendations['composite_score'].mean(), 1),
            'high_confidence_count': len(recommendations[recommendations['confidence'] == 'High']),
            'last_updated': last_update.isoformat() if last_update else None,
            'total_sectors': len(Config.STOCK_SECTORS)
        }

        # Sector-wise stats
        sector_stats = {}
        for sector_name, stocks in Config.STOCK_SECTORS.items():
            sector_recs = recommendations[recommendations['symbol'].isin(stocks)]
            if not sector_recs.empty:
                sector_stats[sector_name] = {
                    'total': len(sector_recs),
                    'buy': len(sector_recs[sector_recs['recommendation'] == 'BUY']),
                    'sell': len(sector_recs[sector_recs['recommendation'] == 'SELL']),
                    'hold': len(sector_recs[sector_recs['recommendation'] == 'HOLD']),
                    'avg_score': round(sector_recs['composite_score'].mean(), 1)
                }

        stats['sector_stats'] = sector_stats

        return jsonify({
            'status': 'success',
            'stats': stats
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/sector-heatmap')
def api_sector_heatmap():
    """Get sector-wise heatmap data for bullish/bearish analysis"""
    try:
        from config import Config
        recommendations = get_recommendations()

        if recommendations.empty:
            return jsonify({'status': 'error', 'message': 'No data available'})

        # Calculate sector-wise metrics
        sector_data = []

        for sector_name, stocks in Config.STOCK_SECTORS.items():
            # Filter results for this sector
            sector_results = recommendations[recommendations['symbol'].isin(stocks)]

            if len(sector_results) == 0:
                continue

            # Calculate sector metrics
            total_stocks = len(sector_results)
            buy_count = len(sector_results[sector_results['recommendation'] == 'BUY'])
            sell_count = len(sector_results[sector_results['recommendation'] == 'SELL'])
            hold_count = len(sector_results[sector_results['recommendation'] == 'HOLD'])

            # Calculate bullish percentage (BUY recommendations)
            bullish_percentage = (buy_count / total_stocks) * 100 if total_stocks > 0 else 0

            # Calculate average sentiment and composite scores
            avg_sentiment = sector_results['sentiment_score'].mean() if 'sentiment_score' in sector_results.columns else 0
            avg_composite = sector_results['composite_score'].mean() if 'composite_score' in sector_results.columns else 0

            # Calculate average price change (if available)
            avg_price_change = sector_results['price_change'].mean() * 100 if 'price_change' in sector_results.columns else 0

            # Determine sector sentiment (bullish/bearish/neutral)
            if bullish_percentage >= 60:
                sector_sentiment = 'bullish'
                sentiment_color = '#22c55e'  # Green
                sentiment_intensity = min(100, bullish_percentage + 20)
            elif bullish_percentage <= 40:
                sector_sentiment = 'bearish'
                sentiment_color = '#ef4444'  # Red
                sentiment_intensity = min(100, (100 - bullish_percentage) + 20)
            else:
                sector_sentiment = 'neutral'
                sentiment_color = '#f59e0b'  # Yellow
                sentiment_intensity = 50

            # Format sector name for display
            display_name = sector_name.replace('_', ' ').title()

            # Get top performing stock in sector
            top_stock = sector_results.nlargest(1, 'composite_score').iloc[0] if not sector_results.empty else None
            top_stock_info = {
                'symbol': top_stock['symbol'].replace('.NS', '') if top_stock is not None else '',
                'score': round(top_stock['composite_score'], 1) if top_stock is not None else 0
            } if top_stock is not None else {'symbol': '', 'score': 0}

            sector_data.append({
                'sector': sector_name,
                'display_name': display_name,
                'total_stocks': total_stocks,
                'buy_count': buy_count,
                'sell_count': sell_count,
                'hold_count': hold_count,
                'bullish_percentage': round(bullish_percentage, 1),
                'avg_sentiment': round(avg_sentiment, 3),
                'avg_composite': round(avg_composite, 1),
                'avg_price_change': round(avg_price_change, 2),
                'sector_sentiment': sector_sentiment,
                'sentiment_color': sentiment_color,
                'sentiment_intensity': sentiment_intensity,
                'top_stock': top_stock_info,
                'stocks': [stock.replace('.NS', '') for stock in stocks]
            })

        # Sort by bullish percentage (most bullish first)
        sector_data.sort(key=lambda x: x['bullish_percentage'], reverse=True)

        return jsonify({
            'status': 'success',
            'sectors': sector_data,
            'last_updated': last_update.isoformat() if last_update else None
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/sector-comparison-heatmap')
def api_sector_comparison_heatmap():
    """Get sector comparison heatmap showing best to worst performing sectors"""
    try:
        from config import Config

        # Create simulated sector performance data for now
        # In a real implementation, this would analyze each sector
        sector_performance = []

        # Define sector metadata
        sector_metadata = {
            'BANKING': {'name': 'Banking', 'icon': '🏦', 'color': '#007bff'},
            'INFORMATION_TECHNOLOGY': {'name': 'Information Technology', 'icon': '💻', 'color': '#28a745'},
            'ENERGY_OIL_GAS': {'name': 'Energy & Oil Gas', 'icon': '⚡', 'color': '#ffc107'},
            'FMCG_CONSUMER': {'name': 'FMCG & Consumer', 'icon': '🛒', 'color': '#17a2b8'},
            'AUTOMOTIVE': {'name': 'Automotive', 'icon': '🚗', 'color': '#6f42c1'},
            'PHARMACEUTICALS': {'name': 'Pharmaceuticals', 'icon': '💊', 'color': '#e83e8c'},
            'FINANCE_NBFC': {'name': 'Finance & NBFC', 'icon': '💰', 'color': '#fd7e14'},
            'METALS_MINING': {'name': 'Metals & Mining', 'icon': '🏭', 'color': '#6c757d'},
            'INFRASTRUCTURE': {'name': 'Infrastructure', 'icon': '🏗️', 'color': '#20c997'},
            'CEMENT': {'name': 'Cement', 'icon': '🧱', 'color': '#dc3545'}
        }

        # Generate simulated performance data
        import random
        random.seed(42)  # For consistent results

        for sector_key, stocks in Config.STOCK_SECTORS.items():
            if sector_key in sector_metadata:
                # Simulate sector strength (40-85 range for realistic spread)
                base_strength = random.uniform(40, 85)

                # Determine category based on strength
                if base_strength >= 70:
                    category = 'strong_buy'
                    label = 'Strong Buy'
                elif base_strength >= 60:
                    category = 'buy'
                    label = 'Buy'
                elif base_strength >= 50:
                    category = 'moderate_buy'
                    label = 'Moderate Buy'
                elif base_strength >= 40:
                    category = 'hold'
                    label = 'Hold'
                elif base_strength >= 30:
                    category = 'moderate_sell'
                    label = 'Moderate Sell'
                else:
                    category = 'sell'
                    label = 'Sell'

                sector_performance.append({
                    'sector': sector_key,
                    'display_name': sector_metadata[sector_key]['name'],
                    'icon': sector_metadata[sector_key]['icon'],
                    'color': sector_metadata[sector_key]['color'],
                    'sector_strength': round(base_strength, 1),
                    'category': category,
                    'label': label,
                    'stock_count': len(stocks),
                    'description': f"{len(stocks)} stocks analyzed"
                })

        # Sort by sector strength (highest first)
        sector_performance.sort(key=lambda x: x['sector_strength'], reverse=True)

        return jsonify({
            'status': 'success',
            'sectors': sector_performance,
            'total_sectors': len(sector_performance),
            'last_updated': datetime.now().isoformat(),
            'legend': {
                'strong_buy': {'color': '#16a34a', 'label': 'Strong Buy (70-100)', 'icon': '🚀'},
                'buy': {'color': '#22c55e', 'label': 'Buy (60-69)', 'icon': '📈'},
                'moderate_buy': {'color': '#84cc16', 'label': 'Moderate Buy (50-59)', 'icon': '👍'},
                'hold': {'color': '#eab308', 'label': 'Hold (40-49)', 'icon': '⚖️'},
                'moderate_sell': {'color': '#f97316', 'label': 'Moderate Sell (30-39)', 'icon': '👎'},
                'sell': {'color': '#dc2626', 'label': 'Sell (0-29)', 'icon': '📉'}
            }
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
