import yfinance as yf
from app.models import StockData


def fetch_stock_data(symbol: str, period="1d", interval="1m"):
    try:
        data = yf.download(symbol, period=period, interval=interval)
        data = data.reset_index()
        data['date'] = data['Datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        data = data[['Open', 'High',
                     'Low', 'Close',
                     'Volume', 'date']]
        data['symbol'] = symbol
        data.columns = data.columns.str.lower()
        data = data.to_dict('records')
        return [StockData(**item).model_dump() for item in data]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
