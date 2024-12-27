import requests
import pandas as pd
from config import ENDPOINTS, HEADERS

def get_stock_data(ticker, start_date=None, end_date=None):
    """Get EOD stock data from Tiingo"""
    params = {'startDate': start_date, 'endDate': end_date}
    url = ENDPOINTS['eod'].format(ticker=ticker)
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        # Standardize column names for crypto data
        if 'priceData' in df.columns:
            df = pd.json_normalize(df['priceData'])
        df['date'] = pd.to_datetime(df['date'])
        return df
    return None

def get_crypto_data(tickers, start_date=None, end_date=None):
    """Get cryptocurrency data from Tiingo"""
    params = {
        'tickers': ','.join(tickers),
        'startDate': start_date,
        'endDate': end_date
    }
    response = requests.get(ENDPOINTS['crypto'], headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        # Process nested JSON structure
        processed_data = []
        for item in data:
            ticker = item.get('ticker')
            for price_data in item.get('priceData', []):
                price_data['ticker'] = ticker
                processed_data.append(price_data)
        df = pd.DataFrame(processed_data)
        df['date'] = pd.to_datetime(df['date'])
        return df
    return None

def get_company_news(tickers=None, tags=None, limit=10):
    """Get news articles from Tiingo"""
    params = {
        'tickers': ','.join(tickers) if tickers else None,
        'tags': ','.join(tags) if tags else None,
        'limit': limit
    }
    response = requests.get(ENDPOINTS['news'], headers=HEADERS, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return None

def get_fundamentals(ticker):
    """Get fundamental data from Tiingo"""
    url = ENDPOINTS['fundamentals'].format(ticker=ticker)
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return None
