#!/usr/bin/env python3
"""
Quick start script for Stock News Analysis Agent
This script provides a simple way to run the agent with basic functionality
"""

import os
import sys
from datetime import datetime

def check_environment():
    """Check if we're in the virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment detected")
        return True
    else:
        print("⚠ Not in virtual environment. Please activate it first:")
        print("  stock_agent_env\\Scripts\\activate")
        return False

def test_basic_imports():
    """Test if basic packages are available"""
    try:
        import yfinance as yf
        import pandas as pd
        import requests
        from textblob import TextBlob
        print("✓ Core packages imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def quick_stock_test():
    """Test basic stock data fetching"""
    try:
        import yfinance as yf
        print("\nTesting stock data fetching...")
        
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        hist = ticker.history(period="5d")
        
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            print(f"✓ AAPL current price: ${current_price:.2f}")
            return True
        else:
            print("⚠ No stock data returned")
            return False
            
    except Exception as e:
        print(f"✗ Stock data test failed: {e}")
        return False

def quick_sentiment_test():
    """Test basic sentiment analysis"""
    try:
        from textblob import TextBlob
        print("\nTesting sentiment analysis...")
        
        text = "Apple stock surges on strong earnings report"
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        
        print(f"✓ Sentiment analysis working. Sample: {sentiment:.3f}")
        return True
        
    except Exception as e:
        print(f"✗ Sentiment test failed: {e}")
        return False

def run_web_app():
    """Start the web application"""
    try:
        print("\n" + "="*50)
        print("Starting Stock News Analysis Agent Web App...")
        print("="*50)
        
        from app import app
        from config import Config
        
        print(f"🚀 Starting server at http://{Config.HOST}:{Config.PORT}")
        print("Press Ctrl+C to stop the server")
        print("\nFeatures available:")
        print("- Real-time stock analysis")
        print("- News sentiment analysis")
        print("- Buy/Sell/Hold recommendations")
        print("- Interactive charts and dashboard")
        print("\nNote: First run may take longer as it downloads data...")
        
        app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except Exception as e:
        print(f"\n✗ Error starting web app: {e}")
        print("\nTrying command line mode instead...")
        run_command_line()

def run_command_line():
    """Run command line analysis"""
    try:
        print("\n" + "="*50)
        print("Running Command Line Analysis...")
        print("="*50)
        
        from stock_filter import StockFilter
        
        # Test with a few stocks
        test_symbols = ['AAPL', 'MSFT', 'GOOGL']
        print(f"Analyzing {len(test_symbols)} stocks: {', '.join(test_symbols)}")
        
        filter_agent = StockFilter()
        recommendations = filter_agent.analyze_stocks(test_symbols)
        
        if not recommendations.empty:
            print(f"\n✓ Analysis completed! Found {len(recommendations)} recommendations")
            
            # Show top recommendation
            buy_recs = recommendations[recommendations['recommendation'] == 'BUY']
            if not buy_recs.empty:
                top_pick = buy_recs.iloc[0]
                print(f"\n🚀 TOP BUY RECOMMENDATION:")
                print(f"   Symbol: {top_pick['symbol']}")
                print(f"   Score: {top_pick['composite_score']:.1f}/100")
                print(f"   Reasoning: {top_pick['reasoning']}")
                print(f"   Risk Level: {top_pick['risk_level']}")
            
            print(f"\nFor detailed analysis, run: python run_analysis.py")
            print(f"For web interface, run: python app.py")
            
        else:
            print("⚠ No recommendations generated")
            
    except Exception as e:
        print(f"✗ Command line analysis failed: {e}")

def main():
    """Main function"""
    print("Stock News Analysis Agent - Quick Start")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return
    
    # Test imports
    if not test_basic_imports():
        return
    
    # Quick tests
    stock_test_ok = quick_stock_test()
    sentiment_test_ok = quick_sentiment_test()
    
    if not (stock_test_ok and sentiment_test_ok):
        print("\n⚠ Some tests failed. The agent may not work properly.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Ask user what to run
    print("\n" + "="*50)
    print("Choose how to run the agent:")
    print("1. Web Application (recommended)")
    print("2. Command Line Analysis")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            run_web_app()
            break
        elif choice == '2':
            run_command_line()
            break
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
