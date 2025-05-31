#!/usr/bin/env python3
"""
Command-line runner for Stock News Analysis Agent
Use this to run analysis without the web interface
"""

import argparse
import pandas as pd
from datetime import datetime
from config import Config
from stock_filter import StockFilter

def print_recommendations(recommendations_df, action=None, limit=10):
    """Print recommendations in a formatted table"""
    if recommendations_df.empty:
        print("No recommendations found.")
        return
    
    # Filter by action if specified
    if action:
        recommendations_df = recommendations_df[recommendations_df['recommendation'] == action.upper()]
        if recommendations_df.empty:
            print(f"No {action.upper()} recommendations found.")
            return
    
    # Limit results
    recommendations_df = recommendations_df.head(limit)
    
    print(f"\n{'='*100}")
    print(f"{'STOCK RECOMMENDATIONS':<100}")
    print(f"{'='*100}")
    
    # Header
    print(f"{'Symbol':<8} {'Price':<8} {'Change%':<8} {'Sentiment':<10} {'Score':<6} {'Rec':<5} {'Conf':<6} {'Risk':<6} {'Reasoning':<30}")
    print(f"{'-'*100}")
    
    # Data rows
    for _, row in recommendations_df.iterrows():
        symbol = row['symbol']
        price = f"${row['current_price']:.2f}"
        change = f"{row['price_change']:.1f}%"
        sentiment = row['sentiment'][:9]
        score = f"{row['composite_score']:.1f}"
        rec = row['recommendation']
        conf = row['confidence'][:5]
        risk = row['risk_level'][:5]
        reasoning = row['reasoning'][:29]
        
        print(f"{symbol:<8} {price:<8} {change:<8} {sentiment:<10} {score:<6} {rec:<5} {conf:<6} {risk:<6} {reasoning:<30}")

def print_summary(recommendations_df):
    """Print summary statistics"""
    if recommendations_df.empty:
        print("No data to summarize.")
        return
    
    total = len(recommendations_df)
    buy_count = len(recommendations_df[recommendations_df['recommendation'] == 'BUY'])
    hold_count = len(recommendations_df[recommendations_df['recommendation'] == 'HOLD'])
    sell_count = len(recommendations_df[recommendations_df['recommendation'] == 'SELL'])
    
    avg_sentiment = recommendations_df['sentiment_score'].mean()
    avg_score = recommendations_df['composite_score'].mean()
    
    high_conf = len(recommendations_df[recommendations_df['confidence'] == 'High'])
    
    print(f"\n{'='*50}")
    print(f"{'SUMMARY STATISTICS':<50}")
    print(f"{'='*50}")
    print(f"Total stocks analyzed: {total}")
    print(f"Buy recommendations: {buy_count} ({buy_count/total*100:.1f}%)")
    print(f"Hold recommendations: {hold_count} ({hold_count/total*100:.1f}%)")
    print(f"Sell recommendations: {sell_count} ({sell_count/total*100:.1f}%)")
    print(f"Average sentiment score: {avg_sentiment:.3f}")
    print(f"Average composite score: {avg_score:.1f}")
    print(f"High confidence recommendations: {high_conf}")

def save_to_csv(recommendations_df, filename=None):
    """Save recommendations to CSV file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stock_recommendations_{timestamp}.csv"
    
    recommendations_df.to_csv(filename, index=False)
    print(f"\nRecommendations saved to: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Stock News Analysis Agent - Command Line Interface')
    
    parser.add_argument('--symbols', '-s', nargs='+', 
                       help='Stock symbols to analyze (default: use config list)')
    
    parser.add_argument('--action', '-a', choices=['BUY', 'SELL', 'HOLD'], 
                       help='Filter by recommendation action')
    
    parser.add_argument('--limit', '-l', type=int, default=10,
                       help='Limit number of results to display (default: 10)')
    
    parser.add_argument('--save', '-o', type=str, 
                       help='Save results to CSV file')
    
    parser.add_argument('--no-summary', action='store_true',
                       help='Skip summary statistics')
    
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Reduce output verbosity')
    
    args = parser.parse_args()
    
    # Configure symbols
    symbols = args.symbols if args.symbols else Config.STOCK_SYMBOLS
    
    if not args.quiet:
        print("Stock News Analysis Agent")
        print("=" * 50)
        print(f"Analyzing {len(symbols)} stocks...")
        print(f"Symbols: {', '.join(symbols[:10])}" + ("..." if len(symbols) > 10 else ""))
        print()
    
    try:
        # Run analysis
        stock_filter = StockFilter()
        recommendations = stock_filter.analyze_stocks(symbols)
        
        if recommendations.empty:
            print("No recommendations generated. Check your configuration and try again.")
            return
        
        # Display results
        if not args.no_summary:
            print_summary(recommendations)
        
        print_recommendations(recommendations, args.action, args.limit)
        
        # Save to file if requested
        if args.save:
            save_to_csv(recommendations, args.save)
        
        # Show top picks
        if not args.quiet and not args.action:
            buy_recs = recommendations[recommendations['recommendation'] == 'BUY']
            if not buy_recs.empty:
                print(f"\n🚀 TOP BUY RECOMMENDATION:")
                top_pick = buy_recs.iloc[0]
                print(f"   {top_pick['symbol']} - Score: {top_pick['composite_score']:.1f}")
                print(f"   Reasoning: {top_pick['reasoning']}")
                print(f"   Risk Level: {top_pick['risk_level']}")
        
        print(f"\nAnalysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
    except Exception as e:
        print(f"Error during analysis: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
