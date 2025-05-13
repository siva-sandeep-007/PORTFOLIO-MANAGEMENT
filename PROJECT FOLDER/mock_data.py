import random
from datetime import datetime, timedelta

# Mock stock data with realistic current market prices
STOCKS = {
    'AAPL': {
        'name': 'Apple Inc.',
        'price': 185.92,
        'change': 1.25,
        'volume': 58743210,
        'market_cap': '2.9T',
        'sector': 'Technology'
    },
    'GOOGL': {
        'name': 'Alphabet Inc.',
        'price': 142.56,
        'change': -0.85,
        'volume': 25432100,
        'market_cap': '1.8T',
        'sector': 'Technology'
    },
    'MSFT': {
        'name': 'Microsoft Corporation',
        'price': 415.32,
        'change': 2.15,
        'volume': 32456780,
        'market_cap': '3.1T',
        'sector': 'Technology'
    },
    'AMZN': {
        'name': 'Amazon.com Inc.',
        'price': 178.75,
        'change': 1.45,
        'volume': 45678900,
        'market_cap': '1.8T',
        'sector': 'Consumer Cyclical'
    },
    'TSLA': {
        'name': 'Tesla Inc.',
        'price': 175.34,
        'change': -2.15,
        'volume': 98765430,
        'market_cap': '556B',
        'sector': 'Automotive'
    },
    'NVDA': {
        'name': 'NVIDIA Corporation',
        'price': 875.28,
        'change': 3.45,
        'volume': 45678900,
        'market_cap': '2.1T',
        'sector': 'Technology'
    },
    'META': {
        'name': 'Meta Platforms Inc.',
        'price': 485.58,
        'change': 1.85,
        'volume': 23456780,
        'market_cap': '1.2T',
        'sector': 'Technology'
    },
    'JPM': {
        'name': 'JPMorgan Chase & Co.',
        'price': 195.43,
        'change': 0.75,
        'volume': 12345670,
        'market_cap': '562B',
        'sector': 'Financial Services'
    }
}

# Mock news data
def generate_news(ticker):
    news_templates = {
        'AAPL': [
            "Apple announces new {product} with revolutionary features",
            "Apple's {product} sales exceed expectations",
            "Apple stock rises on {product} success",
            "Analysts bullish on Apple's {product} strategy"
        ],
        'GOOGL': [
            "Google launches new {product} service",
            "Alphabet's {product} division shows strong growth",
            "Google expands {product} capabilities",
            "Analysts predict {product} will drive Google's growth"
        ],
        'MSFT': [
            "Microsoft unveils new {product} features",
            "Microsoft's {product} division reports record revenue",
            "Microsoft expands {product} offerings",
            "Analysts optimistic about Microsoft's {product} strategy"
        ],
        'AMZN': [
            "Amazon launches new {product} service",
            "Amazon's {product} division shows strong growth",
            "Amazon expands {product} capabilities",
            "Analysts predict {product} will drive Amazon's growth"
        ]
    }
    
    products = {
        'AAPL': ['iPhone', 'MacBook', 'iPad', 'Apple Watch', 'AirPods'],
        'GOOGL': ['Cloud', 'AI', 'Search', 'Android', 'Chrome'],
        'MSFT': ['Windows', 'Azure', 'Office', 'Xbox', 'Surface'],
        'AMZN': ['AWS', 'Prime', 'Alexa', 'Kindle', 'Fresh']
    }
    
    news = []
    for _ in range(10):
        template = random.choice(news_templates[ticker])
        product = random.choice(products[ticker])
        title = template.format(product=product)
        
        # Generate random date within last 7 days
        date = datetime.now() - timedelta(days=random.randint(0, 7))
        
        news.append({
            'title': title,
            'url': f'https://example.com/news/{ticker.lower()}/{random.randint(1000, 9999)}',
            'date': date.strftime('%Y-%m-%d %H:%M'),
            'source': random.choice(['Bloomberg', 'Reuters', 'CNBC', 'WSJ', 'Financial Times'])
        })
    
    return news

# Mock user portfolio data with realistic holdings
USERS = {
    'admin@example.com': {
        'password': 'admin123',
        'name': 'Admin User',
        'portfolio': {
            'AAPL': {'shares': 100, 'avg_price': 150.00},
            'GOOGL': {'shares': 50, 'avg_price': 140.00},
            'MSFT': {'shares': 75, 'avg_price': 300.00},
            'NVDA': {'shares': 25, 'avg_price': 400.00},
            'TSLA': {'shares': 30, 'avg_price': 200.00}
        }
    }
}

# Mock historical price data
def generate_historical_prices(ticker, days=30):
    base_price = STOCKS[ticker]['price']
    prices = []
    dates = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i)
        # Generate random price movement
        price = base_price * (1 + random.uniform(-0.02, 0.02))
        prices.append(round(price, 2))
        dates.append(date.strftime('%Y-%m-%d'))
    
    return {'dates': dates, 'prices': prices}

# Update the dashboard route in app.py to use more realistic portfolio data
def get_portfolio_data():
    portfolio = []
    for item in [
        {'ticker': 'AAPL', 'shares': 100, 'avg_price': 150.00},
        {'ticker': 'GOOGL', 'shares': 50, 'avg_price': 140.00},
        {'ticker': 'MSFT', 'shares': 75, 'avg_price': 300.00},
        {'ticker': 'NVDA', 'shares': 25, 'avg_price': 400.00},
        {'ticker': 'TSLA', 'shares': 30, 'avg_price': 200.00}
    ]:
        ticker = item['ticker']
        shares = item['shares']
        avg_price = item['avg_price']
        current_price = STOCKS[ticker]['price']
        name = STOCKS[ticker]['name']
        current_value = shares * current_price
        invested = shares * avg_price
        gain_loss = current_value - invested
        gain_loss_percent = (gain_loss / invested) * 100 if invested else 0
        portfolio.append({
            'ticker': ticker,
            'name': name,
            'shares': shares,
            'avg_price': avg_price,
            'current_price': current_price,
            'current_value': current_value,
            'gain_loss': gain_loss,
            'gain_loss_percent': gain_loss_percent
        })
    total_value = sum(item['current_value'] for item in portfolio)
    return portfolio, total_value 