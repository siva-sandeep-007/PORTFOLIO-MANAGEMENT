from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from textblob import TextBlob
import plotly
import plotly.graph_objects as go
import json
import nltk
from datetime import datetime
from mock_data import STOCKS, generate_news, USERS, generate_historical_prices, get_portfolio_data
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

# Download required NLTK data
nltk.download('punkt')

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        print(f"Login attempt for username: {username}")  # Debug log
        
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            print("User not found")  # Debug log
            flash('Username not found!', 'error')
            return redirect(url_for('login'))
            
        if not user.check_password(password):
            print("Invalid password")  # Debug log
            flash('Invalid password!', 'error')
            return redirect(url_for('login'))
            
        print("Login successful")  # Debug log
        login_user(user, remember=remember)
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    from mock_data import STOCKS, get_portfolio_data
    
    # Get realistic portfolio data
    portfolio, portfolio_value = get_portfolio_data()
    
    return render_template(
        'dashboard.html',
        portfolio_value=portfolio_value,
        portfolio=portfolio,
        stocks=STOCKS
    )

@app.route('/portfolio')
@login_required
def portfolio():
    from mock_data import get_portfolio_data
    portfolio, portfolio_value = get_portfolio_data()
    return render_template('portfolio.html', portfolio=portfolio, portfolio_value=portfolio_value)

@app.route('/analyze/<ticker>')
def analyze(ticker):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if ticker not in STOCKS:
        return redirect(url_for('dashboard'))
    
    news_data = generate_news(ticker)
    analyzed_news = []
    
    for news in news_data:
        sentiment, score = analyze_sentiment(news['title'])
        analyzed_news.append({
            'title': news['title'],
            'url': news['url'],
            'sentiment': sentiment,
            'score': score,
            'date': news['date'],
            'source': news['source']
        })
    
    sentiment_chart = create_sentiment_chart(analyzed_news)
    price_chart = create_price_chart(ticker)
    
    return render_template(
        'analysis.html',
        ticker=ticker,
        stock=STOCKS[ticker],
        news=analyzed_news,
        sentiment_chart=sentiment_chart,
        price_chart=price_chart
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(f"Registration attempt for username: {username}, email: {email}")  # Debug log

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        # Create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"User created successfully: {username}")  # Debug log
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {str(e)}")  # Debug log
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

def analyze_sentiment(text):
    """Analyze sentiment of text using TextBlob"""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        return "positive", polarity
    elif polarity < -0.1:
        return "negative", polarity
    else:
        return "neutral", polarity

def create_sentiment_chart(news_data):
    """Create a bar chart for sentiment analysis"""
    sentiments = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }
    
    for news in news_data:
        sentiment, _ = analyze_sentiment(news['title'])
        sentiments[sentiment] += 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(sentiments.keys()),
            y=list(sentiments.values()),
            marker_color=['green', 'red', 'gray']
        )
    ])
    
    fig.update_layout(
        title="News Sentiment Distribution",
        xaxis_title="Sentiment",
        yaxis_title="Count",
        template="plotly_dark"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_price_chart(ticker):
    """Create a line chart for historical prices"""
    historical_data = generate_historical_prices(ticker)
    
    fig = go.Figure(data=[
        go.Scatter(
            x=historical_data['dates'],
            y=historical_data['prices'],
            mode='lines',
            name=ticker,
            line=dict(color='#00ff00', width=2)
        )
    ])
    
    fig.update_layout(
        title=f"{ticker} Historical Prices",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        showlegend=True
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Initialize database and create tables
with app.app_context():
    db.create_all()
    # Check if we have any users
    user_count = User.query.count()
    print(f"Current number of users in database: {user_count}")  # Debug log

if __name__ == '__main__':
    app.run(debug=True) 