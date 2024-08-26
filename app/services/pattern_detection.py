import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import numpy as np
    
import os


###############################################################
######################### Double Top ##########################
    
def double_top_pattern_detection(data,similarity_threshold = 0.02):
    
    # Identify local maxima (peaks)
    peaks, _ = find_peaks(data['Close'], distance=10)  # distance parameter controls how Close peaks can be

    # print(data)
    # Filter peaks with minimum prominence to ensure they are significant
    peaks, properties = find_peaks(data['Close'], prominence=1, distance=10)
    # print(peaks, properties)
    data['Peak'] = None
    # print(data.iloc[peaks])

    data.loc[peaks, 'Peak'] = data.iloc[peaks].Close

    # Define a list to store detected double tops
    double_tops = []

    # Parameters for double top detection
    # similarity_threshold = 0.02  # 2% similarity between peaks

    # Loop through identified peaks to find double tops
    for i in range(1, len(peaks) - 1):
        # First peak
        first_peak_idx = peaks[i - 1]
        first_peak_value = data['Close'].iloc[first_peak_idx]
        
        # Second peak
        second_peak_idx = peaks[i]
        second_peak_value = data['Close'].iloc[second_peak_idx]
        
        # Check if the two peaks are similar
        if abs((second_peak_value - first_peak_value) / first_peak_value) < similarity_threshold:
            # Find the trough between the two peaks
            trough_idx = data['Close'].iloc[first_peak_idx:second_peak_idx].idxmin()
            trough_value = data['Close'].iloc[trough_idx]
            
            # Confirm the double top if the second peak is folLowed by a significant drop
            post_second_peak_drop = data['Close'].iloc[second_peak_idx:second_peak_idx + 20].min()
            if post_second_peak_drop < trough_value:
                double_tops.append({
                    'first_peak': first_peak_idx,
                    'second_peak': second_peak_idx,
                    'trough': trough_idx,
                    'breakdown': data.index[second_peak_idx + np.argmin(data['Close'].iloc[second_peak_idx:second_peak_idx + 20])]
                })

    # Convert detected patterns to a DataFrame
    double_tops_df = pd.DataFrame(double_tops)
    # print(double_tops_df)
    return double_tops_df
   

def detect_patterns(symbol, pattern_type,period='1y', interval='1d'):
    
    ticker = yf.Ticker(symbol)    
    
    data = ticker.history(period=period.lower, interval = interval.lower)  # Adjust as needed

    if interval[-1].lower == 'm':
        data['Date'] = data['Datetime']
        data = data[
            ['Open', 
             'High',
             'Low', 
             'Close',
             'Volume', 
             'Date']
            ]
        
    data['Symbol'] = symbol

    data = data.dropna()

    data = data.reset_index()

    

    plt.figure(figsize=(14, 7))

    # Create a new stock_pricesFrame called "up" that stores the stock_prices
    # when the closing stock price is greater than the opening stock price
    up = data[data.close >= data.open]

    # Create a new stock_pricesFrame called "down" that stores the stock_prices
    # when the closing stock price is lesser than the opening stock price
    down = data[data.close < data.open]

    ##Green Candles
    plt.bar(x=up.date,height=up["close"] - up["open"], bottom=up["open"], color='green')
    plt.vlines(x=up.date, 
               ymin=up["low"], 
               ymax=up["high"],
               color="green")
    

    ##Red Candles
    plt.bar(x=down.date,height=down["open"] - down["close"], bottom=down["close"],  color="red")
    plt.vlines(x=down.date, 
               ymin=down["low"], 
               ymax=down["high"], 
               color="red")

    # Rotate the x-axis tick labels at 45 degrees towards right
    plt.xticks(rotation=45, ha='right')

    
    # Implement logic for detecting patterns
    if pattern_type == 'double_top':
        # Logic to detect double toppass
        double_tops_df = double_top_pattern_detection(data)
        
        #Plot double top 
        for _, row in double_tops_df.iterrows():
            plt.plot([data['Date'].iloc[row['first_peak']], data['Date'].iloc[row['second_peak']]], 
                    [data['Close'].iloc[row['first_peak']], data['Close'].iloc[row['second_peak']]], 
                    'ro-', lw=2 )
            plt.plot(data['Date'].iloc[row['trough']], data['Close'].iloc[row['trough']], 'go', markersize=8)
            plt.plot(data['Date'].loc[row['breakdown']], data['Close'].iloc[row['breakdown']], 'bo', markersize=8 )


    elif pattern_type == 'support':
        # def detect_support_resistance(data, window=14, threshold=0.02):
        # Calculate rolling min and max for support and resistance
        window=9
        
        support_level = data[data['low']== data['low'].rolling(window=window,center=True).min()]
        support_level = support_level[abs(support_level['low'].diff())>.100]

        # plot support lines
        plt.hlines(support_level['low'],xmax=support_level['date'].shift(-1), xmin=support_level['date'], color='green', label="Support Line")


    elif pattern_type == 'resistance':
        # Logic to detect resistance linepass

        window=9
        
        resistance_level = data[data['high']== data['high'].rolling(window=window,center=True).max()]
    
        resistance_level = resistance_level[abs(resistance_level['high'].diff())>.100]

        # plot resistance lines
        plt.hlines(resistance_level['high'],xmax=resistance_level['date'].shift(-1), xmin=resistance_level['date'], color='red', label="Resistance Line")

    else:
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