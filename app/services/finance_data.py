import yfinance as yf
from app.models import StockData
import pandas as pd

def get_financial_data(symbol):
    ticker = yf.Ticker(symbol)   
    print("hello") 
    data = {        
        'price': ticker.history(period="1d").to_dict(),
        'financials': ticker.financials.to_dict(),
        'balance_sheet': ticker.balance_sheet.to_dict(),
        'cashflow': ticker.cashflow.to_dict(),
        # Add more segmented data as needed
    }
    [StockData(**item).model_dump() for item in data['price']]
    return data

    # try:

    #     data = pd.read_json("/home/nishant.barevadiya/Work/flask-fintech/response_1.json")
    #     data = data.reset_index()
    #     data = data[['Open', 'High',
    #                  'Low', 'Close', 'Volume', 'date']]
    #     data['symbol'] = symbol
    #     data.columns = data.columns.str.lower()
    #     data = data.to_dict('records')
    #     return [StockData(**item).model_dump() for item in data]



    #     period= '1d'
    #     interval = '1m'
    #     data = yf.download(symbol, period=period, interval=interval)
    #     data = data.reset_index()
    #     data['date'] = data['Datetime'].dt.strftime('%Y-%m-%d')
    #     data = data[['Open', 'High',
    #                  'Low', 'Close', 'Volume', 'date']]
    #     data['symbol'] = symbol
    #     data.columns = data.columns.str.lower()
    #     data = data.to_dict('records')
    #     return [StockData(**item).model_dump() for item in data]
    # except Exception as e:
    #     print(f"Error fetching data: {e}")
    #     return []
