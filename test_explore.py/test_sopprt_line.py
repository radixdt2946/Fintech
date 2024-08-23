# # Since the mplfinance package is not available, I'll use an alternative approach using matplotlib directly.
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

# # Function to find support and resistance levels
# def find_support_resistance(data, window=9):
#     supports = []
#     resistances = []
    
#     for i in range(window, len(data) - window):
#         support = min(data['low'][i-window:i+window])
#         resistance = max(data['high'][i-window:i+window])
#         supports.append((data.index[i], support))
#         resistances.append((data.index[i], resistance))
    
#     return supports, resistances


# data = pd.read_csv("/home/nishant.barevadiya/Work/flask-fintech/output.csv")
# # Find support and resistance lines
# supports, resistances = find_support_resistance(data)

# # Plotting the candlestick chart with support and resistance levels
# fig, ax = plt.subplots(figsize=(14, 8))

# # Plot candlestick bars
# for i in range(len(data)):
#     color = 'green' if data['close'][i] >= data['open'][i] else 'red'
#     ax.plot([data.index[i], data.index[i]], [data['low'][i], data['high'][i]], color='black')
#     ax.plot([data.index[i], data.index[i]], [data['open'][i], data['close'][i]], color=color, linewidth=2)

# # Plot support lines
# for support in supports:
#     ax.axhline(y=support[1], color='green', linestyle='--', lw=0.8)

# # Plot resistance lines
# for resistance in resistances:
#     ax.axhline(y=resistance[1], color='red', linestyle='--', lw=0.8)

# # Formatting the date on x-axis
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
# plt.xticks(rotation=45)

# ax.set_title('Support and Resistance Lines on Candlestick Chart')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.grid(True)

# plt.show()


import yfinance as yf

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
    # [StockData(**item).model_dump() for item in data['price']]
    return data

print(get_financial_data('AAPL'))