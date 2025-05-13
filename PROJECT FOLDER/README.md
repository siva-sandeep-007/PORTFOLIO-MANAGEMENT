# Stock Sentiment Analyzer

A Flask-based web application that analyzes news sentiment for stocks and correlates it with market data. The application uses Natural Language Processing (NLP) to analyze news headlines and provides visualizations of sentiment distribution.

## Features

- Real-time stock news retrieval via Mboum Finance API
- Sentiment analysis of news headlines using TextBlob and NLTK
- Interactive visualizations using Plotly
- Clickable news links for full article access
- Modern, responsive user interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Mboum Finance API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stock-sentiment-analyzer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Mboum Finance API key:
```
MBOUM_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter a stock ticker symbol (e.g., AAPL, GOOGL, MSFT) and click "Analyze"

4. View the sentiment analysis results and news articles

## Project Structure

```
stock-sentiment-analyzer/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this file)
├── templates/         # HTML templates
│   ├── index.html    # Home page
│   └── analysis.html # Analysis results page
└── README.md         # This file
```

## Technologies Used

- Flask: Web framework
- TextBlob & NLTK: Natural Language Processing
- Plotly: Data visualization
- Bootstrap: Frontend styling
- Mboum Finance API: Stock data and news

## Future Enhancements

- Integration with Order Management Systems (OMS)
- Advanced machine learning models for sentiment analysis
- Historical sentiment trend analysis
- Real-time sentiment alerts
- Additional data sources for comprehensive analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details. 