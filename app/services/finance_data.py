import yfinance as yf
from app.models import StockData
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_financial_data(symbol: str) -> dict:
    '''
        Fetch financial data from Yahoo Finance API.

        This function retrieves 1-day period stock data, along with financial statements, 
        balance sheet, and cash flow data for a specific stock symbol.

        Fetch financial data from Yahoo Finance API.

        Parameters:
        -----------
        symbol : str
            The stock symbol to fetch data for.
        Returns:
        --------
        dict
            A dictionary containing the stock's price data, financials, balance
        sheet, and cash flow.
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
        logging.error(f"Error fetching data for {symbol}: {e}")
        return {"error": str(e)}
        