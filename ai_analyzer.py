"""
Real AI Stock Analysis using DeepSeek and other free AI models
"""

import requests
import json
import time
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional

class AIStockAnalyzer:
    def __init__(self):
        """Initialize AI analyzer with Groq as primary AI model"""
        self.groq_api_key = None
        self.available_models = []

        # Groq API endpoint (OpenAI compatible)
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

        self._check_available_models()

    def _check_available_models(self):
        """Check which AI models are available - Groq focused"""
        # Try to load API key from environment or config
        try:
            from config import Config
            self.groq_api_key = getattr(Config, 'GROQ_API_KEY', None)
        except:
            pass

        if self.groq_api_key and len(self.groq_api_key) > 10:
            self.available_models.append('groq')
            print("✓ Groq AI available (Primary)")
        else:
            print("⚠ Groq API key not configured")

        # Fallback - Hugging Face transformers (local)
        try:
            import transformers
            self.available_models.append('huggingface')
            print("✓ Hugging Face transformers available (Fallback)")
        except:
            print("○ Hugging Face transformers not available")

        if not self.available_models:
            print("⚠ No AI models available - will use rule-based analysis")
        else:
            print(f"🤖 AI Models ready: {', '.join(self.available_models)}")

    def analyze_stock_with_ai(self, stock_data: Dict, sentiment_data: Dict = None) -> Dict:
        """Analyze stock using real AI models with sentiment integration"""

        if not self.available_models:
            return self._fallback_analysis(stock_data)

        # Prepare data for AI analysis with sentiment context
        analysis_prompt = self._create_analysis_prompt(stock_data, sentiment_data)

        # Try AI models in order of preference (Groq first)
        for model in ['groq', 'huggingface']:
            if model in self.available_models:
                try:
                    result = self._analyze_with_model(analysis_prompt, model)
                    if result:
                        return self._parse_ai_response(result, stock_data)
                except Exception as e:
                    print(f"Error with {model}: {e}")
                    continue

        # Fallback to rule-based
        return self._fallback_analysis(stock_data)

    def _create_analysis_prompt(self, stock_data: Dict, sentiment_data: Dict = None) -> str:
        """Create comprehensive prompt for AI analysis with sentiment integration"""

        symbol = stock_data.get('symbol', 'Unknown')
        price = stock_data.get('current_price', 0)
        change = stock_data.get('price_change', 0) * 100
        market_cap = stock_data.get('market_cap', 0)
        pe_ratio = stock_data.get('pe_ratio', 'N/A')
        rsi = stock_data.get('rsi', 50)
        sector = stock_data.get('sector', 'Unknown')

        # Extract sentiment information
        if sentiment_data:
            sentiment_score = sentiment_data.get('sentiment_score', 0)
            overall_sentiment = sentiment_data.get('overall_sentiment', 'neutral')
            article_count = sentiment_data.get('article_count', 0)
            confidence = sentiment_data.get('confidence', 0)
        else:
            sentiment_score = 0
            overall_sentiment = 'neutral'
            article_count = 0
            confidence = 0

        prompt = f"""
You are a professional Indian stock market analyst. Analyze the following stock and provide detailed investment insights.

STOCK: {symbol}
SECTOR: {sector}
CURRENT PRICE: ₹{price}
PRICE CHANGE: {change:+.2f}%
MARKET CAP: ₹{market_cap/1e7:.1f} Crores
P/E RATIO: {pe_ratio}
RSI: {rsi}

TECHNICAL INDICATORS:
- RSI (14): {rsi:.1f} {"(Oversold)" if rsi < 30 else "(Overbought)" if rsi > 70 else "(Neutral)"}
- Moving Averages: SMA20: ₹{stock_data.get('ma_20', price):.1f}, SMA50: ₹{stock_data.get('ma_50', price):.1f}
- Exponential MAs: EMA20: ₹{stock_data.get('ema_20', price):.1f}, EMA50: ₹{stock_data.get('ema_50', price):.1f}
- MACD: Line: {stock_data.get('macd_line', 0):.2f}, Signal: {stock_data.get('macd_signal', 0):.2f}
- Bollinger Bands: Upper: ₹{stock_data.get('bb_upper', price):.1f}, Lower: ₹{stock_data.get('bb_lower', price):.1f}
- Stochastic: %K: {stock_data.get('stoch_k', 50):.1f}, %D: {stock_data.get('stoch_d', 50):.1f}
- Volume Ratio: {stock_data.get('volume_ratio', 1.0):.1f}x
- Volatility: {stock_data.get('volatility', 0)*100:.2f}%

FINANCIAL HEALTH:
- Dividend Yield: {stock_data.get('dividend_yield', 0):.2f}%
- Price-to-Book: {stock_data.get('pb_ratio', 'N/A')}
- Return on Equity: {stock_data.get('roe', 'N/A')}
- Debt-to-Equity: {stock_data.get('debt_to_equity', 'N/A')}
- Current Ratio: {stock_data.get('current_ratio', 'N/A')}

MARKET SENTIMENT ANALYSIS:
- Overall Sentiment: {overall_sentiment.upper()}
- Sentiment Score: {sentiment_score:+.3f} (range: -1 to +1)
- News Articles Analyzed: {article_count}
- Sentiment Confidence: {confidence:.2f}
- Sentiment Impact: {"POSITIVE" if sentiment_score > 0.1 else "NEGATIVE" if sentiment_score < -0.1 else "NEUTRAL"}

Please provide a comprehensive analysis including:

1. INVESTMENT RECOMMENDATION (BUY/HOLD/SELL) with confidence level
2. TARGET PRICE with reasoning based on technical and fundamental analysis
3. RISK LEVEL (Low/Medium/High) with explanation
4. TIME HORIZON (Short/Medium/Long term)
5. KEY CATALYSTS (3-5 positive factors)
6. RISK FACTORS (3-5 concerns to watch)
7. COMPREHENSIVE TECHNICAL ANALYSIS:
   - Moving Average Analysis (SMA vs EMA trends)
   - MACD signals and momentum
   - RSI overbought/oversold conditions
   - Bollinger Bands position analysis
   - Stochastic oscillator signals
   - Volume and volatility assessment
8. FUNDAMENTAL ANALYSIS:
   - Valuation metrics (P/E, P/B ratios)
   - Financial health (ROE, debt ratios)
   - Dividend analysis and yield attractiveness
   - Liquidity ratios and financial stability
9. SENTIMENT INTEGRATION - How news sentiment affects your analysis
10. INVESTMENT THESIS (2-3 sentences combining technical, fundamental, and sentiment factors)

Focus on Indian market context, considering:
- NSE/BSE listing dynamics
- Indian economic factors
- Sector-specific trends in India
- Regulatory environment
- Market sentiment impact on stock performance
- News-driven price movements in Indian markets

Respond in JSON format:
{{
    "recommendation": "BUY/HOLD/SELL",
    "confidence": "High/Medium/Low",
    "target_price": number,
    "risk_level": "Low/Medium/High",
    "time_horizon": "Short/Medium/Long",
    "catalysts": ["factor1", "factor2", "factor3"],
    "risks": ["risk1", "risk2", "risk3"],
    "technical_summary": "brief technical analysis",
    "investment_thesis": "detailed reasoning",
    "ai_score": number_0_to_100
}}
"""

        return prompt

    def _analyze_with_model(self, prompt: str, model: str) -> Optional[str]:
        """Analyze using specific AI model"""

        if model == 'groq':
            return self._analyze_with_groq(prompt)
        elif model == 'huggingface':
            return self._analyze_with_huggingface(prompt)

        return None



    def _analyze_with_groq(self, prompt: str) -> Optional[str]:
        """Analyze using Groq API with best available models"""

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }

        # Try multiple models in order of preference (best to fallback)
        models_to_try = [
            "llama-3.1-70b-versatile",  # Best reasoning model
            "llama-3.1-8b-instant",     # Faster alternative
            "mixtral-8x7b-32768",       # Good for analysis
            "gemma-7b-it"               # Fallback option
        ]

        for model in models_to_try:
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert Indian stock market analyst with deep knowledge of NSE/BSE markets, Indian economy, sector dynamics, and financial analysis. Provide detailed, professional investment analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 2000,
                "top_p": 0.9
            }

            try:
                print(f"🤖 Analyzing with Groq model: {model}")
                response = requests.post(self.groq_url, headers=headers, json=data, timeout=30)
                response.raise_for_status()

                result = response.json()
                content = result['choices'][0]['message']['content']

                if content and len(content) > 100:  # Ensure we got a substantial response
                    print(f"✓ Groq analysis completed with {model}")
                    return content
                else:
                    print(f"⚠ Short response from {model}, trying next model")
                    continue

            except Exception as e:
                print(f"✗ Error with {model}: {e}")
                continue

        print("✗ All Groq models failed")
        return None

    def _analyze_with_huggingface(self, prompt: str) -> Optional[str]:
        """Analyze using local Hugging Face model"""

        try:
            from transformers import pipeline

            # Use a smaller model for local inference
            generator = pipeline("text-generation",
                               model="microsoft/DialoGPT-medium",
                               max_length=500)

            # Simplified prompt for smaller model
            simple_prompt = f"Analyze stock with price change {prompt[:200]}..."

            result = generator(simple_prompt, max_length=300, num_return_sequences=1)
            return result[0]['generated_text']

        except Exception as e:
            print(f"Hugging Face error: {e}")
            return None

    def _parse_ai_response(self, ai_response: str, stock_data: Dict) -> Dict:
        """Parse AI response and extract structured data"""

        try:
            # Try to extract JSON from response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1

            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                ai_analysis = json.loads(json_str)
            else:
                # Fallback parsing
                ai_analysis = self._parse_text_response(ai_response)

            # Ensure all required fields exist
            return {
                'recommendation': ai_analysis.get('recommendation', 'HOLD'),
                'confidence': ai_analysis.get('confidence', 'Medium'),
                'target_price': ai_analysis.get('target_price', stock_data.get('current_price', 0)),
                'risk_level': ai_analysis.get('risk_level', 'Medium'),
                'time_horizon': ai_analysis.get('time_horizon', 'Medium'),
                'catalysts': ai_analysis.get('catalysts', ['Market growth', 'Sector expansion']),
                'risks': ai_analysis.get('risks', ['Market volatility', 'Economic uncertainty']),
                'technical_summary': ai_analysis.get('technical_summary', 'Mixed signals'),
                'investment_thesis': ai_analysis.get('investment_thesis', 'Moderate investment potential'),
                'ai_score': ai_analysis.get('ai_score', 50),
                'analysis_source': 'AI',
                'analysis_timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._fallback_analysis(stock_data)

    def _parse_text_response(self, response: str) -> Dict:
        """Parse non-JSON AI response"""

        # Simple text parsing for non-JSON responses
        analysis = {}

        if 'BUY' in response.upper():
            analysis['recommendation'] = 'BUY'
        elif 'SELL' in response.upper():
            analysis['recommendation'] = 'SELL'
        else:
            analysis['recommendation'] = 'HOLD'

        # Extract other fields with simple pattern matching
        # This is a simplified implementation
        analysis['confidence'] = 'Medium'
        analysis['risk_level'] = 'Medium'
        analysis['time_horizon'] = 'Medium'
        analysis['catalysts'] = ['AI identified growth potential']
        analysis['risks'] = ['Market volatility']
        analysis['technical_summary'] = 'AI analysis completed'
        analysis['investment_thesis'] = response[:200] + '...' if len(response) > 200 else response
        analysis['ai_score'] = 60

        return analysis

    def _fallback_analysis(self, stock_data: Dict) -> Dict:
        """Fallback rule-based analysis when AI is not available"""

        price_change = stock_data.get('price_change', 0)
        rsi = stock_data.get('rsi', 50)

        # Simple rule-based recommendation
        if price_change > 0.02 and rsi < 70:
            recommendation = 'BUY'
            confidence = 'Medium'
        elif price_change < -0.02 and rsi > 30:
            recommendation = 'SELL'
            confidence = 'Medium'
        else:
            recommendation = 'HOLD'
            confidence = 'Low'

        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'target_price': stock_data.get('current_price', 0) * 1.1,
            'risk_level': 'Medium',
            'time_horizon': 'Medium',
            'catalysts': ['Technical indicators', 'Market momentum'],
            'risks': ['Market volatility', 'Economic factors'],
            'technical_summary': f'RSI: {rsi}, Price change: {price_change*100:.2f}%',
            'investment_thesis': 'Rule-based analysis based on technical indicators',
            'ai_score': 50,
            'analysis_source': 'Rule-based',
            'analysis_timestamp': datetime.now().isoformat()
        }

# Test function
def test_ai_analyzer():
    """Test the AI analyzer"""
    analyzer = AIStockAnalyzer()

    # Sample stock data
    sample_stock = {
        'symbol': 'RELIANCE.NS',
        'current_price': 2500,
        'price_change': 0.025,
        'market_cap': 1500000000000,
        'pe_ratio': 15.5,
        'rsi': 65,
        'sector': 'Energy',
        'ma_20': 2480,
        'ma_50': 2450,
        'volume_ratio': 1.2,
        'volatility': 0.25
    }

    result = analyzer.analyze_stock_with_ai(sample_stock)
    print("AI Analysis Result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_ai_analyzer()
