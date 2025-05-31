"""
Debug script to identify the exact issue with Stock Filter Integration
"""

def debug_stock_filter():
    """Debug the stock filter integration step by step"""
    print("🔍 Debugging Stock Filter Integration...")
    
    try:
        print("Step 1: Testing imports...")
        
        # Test individual imports
        try:
            import pandas as pd
            print("✓ pandas imported")
        except Exception as e:
            print(f"✗ pandas import failed: {e}")
            return False
        
        try:
            import numpy as np
            print("✓ numpy imported")
        except Exception as e:
            print(f"✗ numpy import failed: {e}")
            return False
        
        try:
            from datetime import datetime
            print("✓ datetime imported")
        except Exception as e:
            print(f"✗ datetime import failed: {e}")
            return False
        
        try:
            from config import Config
            print("✓ config imported")
        except Exception as e:
            print(f"✗ config import failed: {e}")
            return False
        
        print("\nStep 2: Testing config attributes...")
        
        # Test config attributes
        required_attrs = [
            'USE_AI_ANALYSIS',
            'GROQ_API_KEY', 
            'MIN_VOLUME_RATIO',
            'MIN_NEWS_ARTICLES',
            'MAX_RECOMMENDATIONS',
            'STOCK_SYMBOLS'
        ]
        
        for attr in required_attrs:
            try:
                value = getattr(Config, attr, 'NOT_FOUND')
                print(f"✓ Config.{attr} = {value}")
            except Exception as e:
                print(f"✗ Config.{attr} failed: {e}")
        
        print("\nStep 3: Testing component imports...")
        
        # Test component imports one by one
        components = [
            ('enhanced_indian_news_collector', 'EnhancedIndianNewsCollector'),
            ('stock_data', 'StockDataCollector'),
            ('sentiment_analyzer', 'SentimentAnalyzer'),
            ('ai_analyzer', 'AIStockAnalyzer')
        ]
        
        for module_name, class_name in components:
            try:
                module = __import__(module_name)
                cls = getattr(module, class_name)
                print(f"✓ {module_name}.{class_name} imported")
            except Exception as e:
                print(f"✗ {module_name}.{class_name} failed: {e}")
                return False
        
        print("\nStep 4: Testing StockFilter class...")
        
        try:
            from stock_filter import StockFilter
            print("✓ StockFilter class imported")
        except Exception as e:
            print(f"✗ StockFilter import failed: {e}")
            print(f"Error details: {str(e)}")
            return False
        
        print("\nStep 5: Testing StockFilter initialization...")
        
        try:
            filter_instance = StockFilter()
            print("✓ StockFilter initialized successfully")
            
            # Check AI analyzer
            if hasattr(filter_instance, 'ai_analyzer'):
                if filter_instance.ai_analyzer:
                    print("✓ AI Analyzer is available")
                else:
                    print("○ AI Analyzer is None (AI disabled or no API key)")
            else:
                print("✗ ai_analyzer attribute missing")
                
            return True
            
        except Exception as e:
            print(f"✗ StockFilter initialization failed: {e}")
            print(f"Error details: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    except Exception as e:
        print(f"✗ Debug failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_stock_filter()
    if success:
        print("\n🎉 Stock Filter debugging completed successfully!")
        print("The issue might be in the test script itself.")
    else:
        print("\n❌ Stock Filter has issues that need to be fixed.")
