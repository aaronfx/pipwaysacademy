import requests
import json
import base64
from flask import current_app

def call_openrouter_api(messages, temperature=0.7):
    """Make API call to OpenRouter"""
    headers = {
        'Authorization': f'Bearer {current_app.config["OPENROUTER_API_KEY"]}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://tradingacademy.com',
        'X-Title': 'Trading Academy AI Analysis'
    }
    
    data = {
        'model': current_app.config['AI_MODEL'],
        'messages': messages,
        'temperature': temperature,
        'max_tokens': 4000
    }
    
    try:
        response = requests.post(
            current_app.config['OPENROUTER_API_URL'],
            headers=headers,
            json=data,
            timeout=120
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def analyze_trade_results(trade_data):
    """Analyze trading results and provide comprehensive feedback"""
    
    system_prompt = """You are an expert trading mentor with 20+ years of experience. Analyze the provided trading data and provide detailed feedback.
    
    You must respond with a valid JSON object containing the following structure:
    {
        "trader_score": <number 0-100>,
        "classification": "<one of: Beginner trader, Scalper, Intraday trader, Swing trader, Position trader, Overtrader, Risky trader, Consistent trader>",
        "win_rate": <number>,
        "risk_reward_ratio": <number>,
        "trade_frequency": "<description>",
        "consistency_score": <number 0-100>,
        "risk_management_score": <number 0-100>,
        "psychology_score": <number 0-100>,
        "strengths": ["<strength 1>", "<strength 2>", ...],
        "weaknesses": ["<weakness 1>", "<weakness 2>", ...],
        "mistakes": ["<mistake 1>", "<mistake 2>", ...],
        "recommendations": ["<recommendation 1>", "<recommendation 2>", ...],
        "improvement_strategy": "<detailed improvement plan>",
        "full_response": "<complete analysis text>"
    }
    
    Be thorough, specific, and actionable in your analysis."""
    
    user_prompt = f"""Please analyze the following trading data and provide a comprehensive assessment:

{trade_data}

Evaluate:
1. Overall performance metrics (win rate, profit factor, etc.)
2. Risk management practices
3. Trading psychology indicators
4. Consistency and discipline
5. Areas of strength and weakness
6. Specific mistakes detected
7. Personalized recommendations for improvement

Provide your response in the exact JSON format specified."""
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    
    response = call_openrouter_api(messages)
    
    if response:
        try:
            # Try to parse JSON response
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            # If not valid JSON, wrap in structure
            return {
                'trader_score': 50,
                'classification': 'Beginner trader',
                'win_rate': None,
                'risk_reward_ratio': None,
                'trade_frequency': 'Unknown',
                'consistency_score': 50,
                'risk_management_score': 50,
                'psychology_score': 50,
                'strengths': ['Analysis completed'],
                'weaknesses': ['Unable to parse detailed metrics'],
                'mistakes': ['Please review data format'],
                'recommendations': ['Consult with trading mentor'],
                'improvement_strategy': response[:1000],
                'full_response': response
            }
    
    # Fallback response
    return {
        'trader_score': 50,
        'classification': 'Beginner trader',
        'win_rate': 0,
        'risk_reward_ratio': 0,
        'trade_frequency': 'Unknown',
        'consistency_score': 50,
        'risk_management_score': 50,
        'psychology_score': 50,
        'strengths': ['System analysis initiated'],
        'weaknesses': ['API connection failed'],
        'mistakes': ['Unable to analyze - technical error'],
        'recommendations': ['Please try again later'],
        'improvement_strategy': 'System temporarily unavailable. Please retry your analysis.',
        'full_response': 'Analysis service temporarily unavailable.'
    }

def analyze_chart_screenshot(image_path):
    """Analyze chart screenshot using vision capabilities"""
    
    # Read and encode image
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    system_prompt = """You are an expert technical analyst and trading mentor. Analyze the provided chart image and provide detailed trading insights.
    
    Respond with a valid JSON object:
    {
        "trader_score": <number 0-100 based on chart quality/setup>,
        "classification": "Chart Analyst",
        "market_structure": "<description of market structure>",
        "trend_direction": "<bullish/bearish/sideways with confidence>",
        "key_levels": {
            "support": ["<level 1>", "<level 2>"],
            "resistance": ["<level 1>", "<level 2>"]
        },
        "possible_entries": ["<entry setup 1>", "<entry setup 2>"],
        "risk_reward_analysis": "<RR assessment>",
        "patterns_identified": ["<pattern 1>", "<pattern 2>"],
        "indicators_analysis": "<indicator interpretation>",
        "strengths": ["<technical strength 1>", "<technical strength 2>"],
        "weaknesses": ["<risk factor 1>", "<risk factor 2>"],
        "mistakes": ["<potential mistake to avoid>"],
        "recommendations": ["<actionable recommendation 1>", "<actionable recommendation 2>"],
        "improvement_strategy": "<how to improve chart reading skills>",
        "full_response": "<complete detailed analysis>"
    }"""
    
    messages = [
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': 'Analyze this trading chart screenshot. Identify market structure, trend, support/resistance levels, possible entry points, and provide trading recommendations. Be specific with price levels if visible.'
                },
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': f'data:image/jpeg;base64,{encoded_image}'
                    }
                }
            ]
        }
    ]
    
    response = call_openrouter_api(messages, temperature=0.5)
    
    if response:
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {
                'trader_score': 70,
                'classification': 'Chart Analyst',
                'market_structure': 'Analysis completed',
                'trend_direction': 'See detailed response',
                'strengths': ['Chart submitted for analysis'],
                'weaknesses': ['Parsing error occurred'],
                'mistakes': ['Technical limitation'],
                'recommendations': ['Review detailed text analysis'],
                'improvement_strategy': response[:1000],
                'full_response': response
            }
    
    return {
        'trader_score': 50,
        'classification': 'Chart Analyst',
        'market_structure': 'Unable to analyze',
        'trend_direction': 'Unknown',
        'strengths': ['Image received'],
        'weaknesses': ['API connection failed'],
        'mistakes': ['Service unavailable'],
        'recommendations': ['Retry analysis'],
        'improvement_strategy': 'Vision analysis service temporarily unavailable.',
        'full_response': 'Chart analysis service unavailable. Please try again later.'
    }
