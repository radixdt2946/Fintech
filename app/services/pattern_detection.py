import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import numpy as np

import os


###############################################################
######################### Double Top ##########################
    
def double_top_pattern_detection(data,similarity_threshold = 0.02):
    '''
        Detect the double top pattern in stock data and return a DataFrame containing the detected patterns.

        Parameters:
        -----------
        data : pd.DataFrame
            A DataFrame containing stock price data. The DataFrame must include a 'Close' column representing 
            the closing prices.
        similarity_threshold : float, optional
            A threshold for comparing the similarity between the two peaks. The default is 0.02 (2% similarity).

    '''
    try:
    
        # Identify local maxima (peaks)
        peaks, _ = find_peaks(data['Close'], distance=10)  # distance parameter controls how Close peaks can be


        # Filter peaks with minimum prominence to ensure they are significant
        peaks, properties = find_peaks(data['Close'], prominence=1, distance=10)

        data['Peak'] = None

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

        return double_tops_df
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return pd.DataFrame()

def detect_patterns(strategy):
    '''
        Detect specific technical patterns in stock data (e.g., Double Top, Support, Resistance).
        generate a candlestick chart, and save the image. The function returns the file path of the 
        saved image or an error message if something goes wrong.


    '''

    try:
        symbol = strategy.get('symbol')
        interval = strategy.get('timeframe', '1d')
        period = strategy.get('period','1y')

        pattern_type = strategy.get('pattern_type')    
        
        ticker = yf.Ticker(symbol)    

        # it check that given ticker symbol is valid or not
        info = ticker.info
        if not info and 'regularMarketPrice' in info:
            return {"error":f'{symbol} is not a valid ticker symbol.',}
        

        data = ticker.history(period=period, interval = interval)  # Adjust as needed

        if data.empty:
            return {"error": f"No data available for {symbol} with the specified timeframe and period."}
        
        data = data.reset_index()

        if str(interval)[-1].lower() == 'm':
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

            
        plt.figure(figsize=(14, 7))

        # Create a new stock_pricesFrame called "up" that stores the stock_prices
        # when the closing stock price is greater than the Opening stock price
        up = data[data.Close >= data.Open]
        
        # Create a new stock_pricesFrame called "down" that stores the stock_prices
        # when the closing stock price is lesser than the Opening stock price
        down = data[data.Close < data.Open]
        try:
            if str(interval)[-1].lower() == 'm':
                width = 0.0004
                ##Green Candles
                plt.bar(x=up.Date,height=up["Close"] - up["Open"],width= width, bottom=up["Open"], color='green')
                plt.vlines(x=up.Date, 
                        ymin=up["Low"], 
                        ymax=up["High"],
                        color="green")
                
                
                ##Red Candles
                plt.bar(x=down.Date,height=down["Open"] - down["Close"], width=width, bottom=down["Close"],  color="red")
                plt.vlines(x=down.Date, 
                        ymin=down["Low"], 
                        ymax=down["High"], 
                        color="red")

            else:
                ##Green Candles
                plt.bar(x=up.Date,height=up["Close"] - up["Open"], bottom=up["Open"], color='green')
                plt.vlines(x=up.Date, 
                            ymin=up["Low"], 
                            ymax=up["High"],
                            color="green")


                ##Red Candles
                plt.bar(x=down.Date,height=down["Open"] - down["Close"], bottom=down["Close"],  color="red")
                plt.vlines(x=down.Date, 
                            ymin=down["Low"], 
                            ymax=down["High"], 
                            color="red")
        except Exception as e:
            return {"error": f"Error plotting candlesticks: {str(e)}"}    
        # Rotate the x-axis tick labels at 45 degrees towards right
        plt.xticks(rotation=45, ha='right')

        
        # Implement logic for detecting patterns
        if str(pattern_type.get("type")).lower() == 'double_top':
            try:
                # Logic to detect double toppass
                similarity_threshold = pattern_type.get('similarity_threshold')
                double_tops_df = double_top_pattern_detection(data, similarity_threshold)

                #Plot double top 
                for _, row in double_tops_df.iterrows():
                    plt.plot([data['Date'].iloc[row['first_peak']], data['Date'].iloc[row['second_peak']]], 
                            [data['Close'].iloc[row['first_peak']], data['Close'].iloc[row['second_peak']]], 
                            'ro-', lw=2 )
                    plt.plot(data['Date'].iloc[row['trough']], data['Close'].iloc[row['trough']], 'go', markersize=8)
                    plt.plot(data['Date'].loc[row['breakdown']], data['Close'].iloc[row['breakdown']], 'bo', markersize=8 )


                plt.title('Double top Pattern')

            except Exception as e:
                return {"error": f"Error detecting double top pattern: {str(e)}"}

        elif str(pattern_type.get("type")).lower() == 'support':
            try:
                # Calculate rolling min and max for support and resistance
                window=pattern_type.get('window')
                
                support_level = data[data['Low']== data['Low'].rolling(window=window,center=True).min()]
                support_level = support_level[abs(support_level['Low'].diff())>.100]

                # plot support lines
                xmax_par = support_level['Date'].shift(-1).fillna(support_level['Date'].iloc[-1])
                plt.hlines(support_level['Low'],xmax=xmax_par, xmin=support_level['Date'], color='green', label="Support Line")

                plt.title('Support level')

            except Exception as e:
                return {"error": f"Error detecting support levels: {str(e)}"}

        elif str(pattern_type.get("type")).lower() == 'resistance':
            try:
                # Logic to detect resistance linepass
                
                window=pattern_type.get('window')
                # similarity_threshold         
                resistance_level = data[data['High']== data['High'].rolling(window=window,center=True).max()]
                
                resistance_level = resistance_level[abs(resistance_level['High'].diff())>.100]
                
                # plot resistance lines
                xmax_par = resistance_level['Date'].shift(-1).fillna(resistance_level['Date'].iloc[-1])

                plt.hlines(resistance_level['High'],xmax=xmax_par, xmin=resistance_level['Date'], color='red', label="Resistance Line")

                plt.title('Resistance level')

            except Exception as e:
                return {"error": f"Error detecting resistance levels: {str(e)}"}
            
        else:
            return {"error":"Invalid pattern type"}
            
        
        # Display the candlestick chart of stock stock_prices and save it in local storage.
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        
        
        # save a graph in given file_path
        file_path = f'assets/{symbol}_{pattern_type.get("type")}.png'
        plt.savefig(file_path)
        
        # plt.show()
        plt.close()
        
        if os.path.exists(file_path):
            return {"file_path": file_path}
        else:
            return {"error": "Failed to save the chart."}
        
        
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}