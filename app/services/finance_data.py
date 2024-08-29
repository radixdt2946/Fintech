import yfinance as yf
from app.models import StockData
import pandas as pd

def get_financial_data(symbol):
    '''
        Fetch financial data from Yahoo Finance API.

        This function retrieves 1-day period stock data, along with financial statements, 
        balance sheet, and cash flow data for a specific stock symbol.
    '''

    try:

        ticker = yf.Ticker(symbol)   
        
        # it check that given ticker symbol is valid or not
        info = ticker.info
        if not info and 'regularMarketPrice' in info:
            return {"error":f'{symbol} is not a valid ticker symbol.',}
        


        stock_data = ticker.history(period='1d')
    
        data = {        
            'price': stock_data.reset_index().to_dict(),
            'financials': ticker.financials.T.reset_index().to_dict(),
            'balance_sheet': ticker.balance_sheet.T.reset_index().to_dict(),
            'cashflow': ticker.cashflow.T.reset_index().to_dict(),
        }
        
        return data
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {"error": str(e)}
        