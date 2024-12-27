import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
TIINGO_API_KEY = os.getenv('TIINGO_API_KEY')
TIINGO_BASE_URL = "https://api.tiingo.com"

# API Endpoints
ENDPOINTS = {
    'meta': f"{TIINGO_BASE_URL}/tiingo/daily/{{ticker}}",
    'eod': f"{TIINGO_BASE_URL}/tiingo/daily/{{ticker}}/prices",
    'crypto': f"{TIINGO_BASE_URL}/tiingo/crypto/prices",
    'news': f"{TIINGO_BASE_URL}/tiingo/news",
    'fundamentals': f"{TIINGO_BASE_URL}/tiingo/fundamentals/{{ticker}}"
}

# Headers for API requests
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {TIINGO_API_KEY}'
}
