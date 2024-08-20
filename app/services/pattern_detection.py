import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
    
import os

def detect_patterns(symbol, pattern_type):
    ticker = yf.Ticker(symbol)    
    data = ticker.history(period="1y")  # Adjust as needed
    # Implement logic for detecting patterns
    if pattern_type == 'double_top':
        # Logic to detect double toppass
        pass

    elif pattern_type == 'support':
        # def detect_support_resistance(data, window=14, threshold=0.02):
        # Calculate rolling min and max for support and resistance
        window=9
        
        support_level = data[data['low']== data['low'].rolling(window=window,center=True).min()]
        support_level = support_level[abs(support_level['low'].diff())>.100]

    elif pattern_type == 'resistance':
        # Logic to detect resistance linepass

        window=9
        
        resistance_level = data[data['high']== data['high'].rolling(window=window,center=True).max()]
    
        resistance_level = resistance_level[abs(resistance_level['high'].diff())>.100]
    
    else:
        # logic to find double top pattern
        pass
        
    plt.figure()

    up = data[data.close >= data.open]

    # Create a new stock_pricesFrame called "down" that stores the stock_prices
    # when the closing stock price is lesser than the opening stock price
    down = data[data.close < data.open]

    # Set the width of candlestick elements
    width = 0.0004


    ##Green Candles
    plt.bar(x=up.date,height=up["close"] - up["open"],width=width, bottom=up["open"], color='green')
    plt.vlines(x=up.date, 
               ymin=up["low"], 
               ymax=up["high"],
               color="green")
    

    ##Red Candles
    plt.bar(x=down.date,height=down["open"] - down["close"],width=width, bottom=down["close"],  color="red")
    plt.vlines(x=down.date, 
               ymin=down["low"], 
               ymax=down["high"], 
               color="red")

    # Rotate the x-axis tick labels at 45 degrees towards right
    plt.xticks(rotation=45, ha='right')

    if support_level :
        # plot support lines
        plt.hlines(support_level['low'],xmax=support_level['date'].shift(-1), xmin=support_level['date'], color='green', label="Support Line")
    elif resistance_level:
        # plot resistance lines
        plt.hlines(resistance_level['high'],xmax=resistance_level['date'].shift(-1), xmin=resistance_level['date'], color='red', label="Resistance Line")
    else:
        #Plot double top 
        pass

    # Display the candlestick chart of stock stock_prices and save it in local storage.
    plt.title('Stock Prices for a Week')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')

    file_path = f'assets/{symbol}_{pattern_type}.png'
    plt.savefig(file_path)
    plt.show()
    plt.close()

    return file_path if os.path.exists(file_path) else None