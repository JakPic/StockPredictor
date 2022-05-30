"""
Module to get list of stocks in NASDAQ, NYSE and AMEX from the NASDAQ stock screener, Querying Yahoo Finance API for the Stock Trading Data and Company Info
"""
#Import packages
import pandas as pd
import requests
import yfinance as yf

# headers and parameters are used to bypass NASDAQ's anti-scraping mechanism in function get_listings
headers = {
    'authority': 'api.nasdaq.com',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'origin': 'https://www.nasdaq.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.nasdaq.com/',
    'accept-language': 'en-US,en;q=0.9',
}

def parameters(exchange):
    return (
        ('letter', '0'),
        ('exchange', exchange),
        ('download', 'true'),
    )

# Get list of stocks in NASDAQ, NYSE and AMEX from the NASDAQ stock screener
def get_listings():
    df_listings=pd.DataFrame()
    EXCHANGES = ['nyse', 'nasdaq', 'amex']
    for exchange in EXCHANGES:
        reqs = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=parameters(exchange))
        #to pick data part of payload
        data = reqs.json()['data']
        temp = pd.DataFrame(data['rows'], columns=data['headers'])
        df_listings=pd.concat([df_listings,temp], ignore_index=True)
    return df_listings
    
#Get Stock Trading Data by querying Yahoo Finance API    
def get_quote(*args):
    if len(args)==2:
        # get historical market data for ticker for given period of time
        hist_data=yf.download(args[0],period=args[1])
    elif len(args)==3:
        # get historical market data for ticker for given range of time
        hist_data = yf.download(args[0],start=args[1],end=args[2])
    return hist_data

#Get Stock Information by querying Yahoo Finance API 
def get_info(_ticker):
    try:
        _yf = yf.Ticker(_ticker)
        # get stock information for ticker
        return _yf.info['longBusinessSummary']
    except:
        return 'No information avaialble.'

def main():
    listings=get_listings()
    _ticker='AMZN'
    stock_data=get_quote(_ticker,'max')

if __name__=="__main__":
    main()