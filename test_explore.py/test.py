# import yfinance as yf
# # from app.models import Stockstock_prices
# import pandas as pd
# ticker = 'AAPL'


# import matplotlib.pyplot as plt
# print("1")
# # try:
    
# stock_prices = pd.read_json("/home/nishant.barevadiya/Work/flask-fintech/response_2.json")
# print(stock_prices)

# stock_prices = stock_prices.reset_index()
# stock_prices = stock_prices[['open', 'high',
#                 'low', 'close', 'volume', 'date']]
# print(stock_prices.describe())
# # print(stock_prices[stock_prices['date']==pd.Timestamp(2024,8,8)])
# stock_prices = stock_prices[stock_prices['date']>pd.Timestamp(2024,8,15,12,0,0)]
# window=10
# threshold=0.5
# stock_prices['rolling_min'] = stock_prices['low'].rolling(window=window, min_periods=1).min()

# support_levels = []
# low=0
# # for i in range(window, len(stock_prices)):
# #     low = stock_prices['low'].iloc[i]
# #     date = stock_prices['date'].iloc[i]
# #     rolling_min = stock_prices['rolling_min'].iloc[i]
    

# #     # Check if current low is within threshold to be a support level
# #     if low <= rolling_min * (1 + threshold):
# #         support_levels.append((stock_prices['date'].iloc[i], low))

# # return support_levels

# # plt.figure(figsize=(14, 7))
# # plt.plot(stock_prices['date'],stock_prices['close'], label=f'{ticker} Close Price', color='blue')
# # plt.plot(support_levels[0],'ro')



# for i in range(window, len(stock_prices) - window):
#     # Look-back period to identify local minimum
#     low_window = stock_prices['low'].iloc[i-window:i]
    
#     # Identify potential support (local minimum)
#     potential_support = low_window.min()
    
#     # Confirm support level
#     next_window_min = stock_prices['low'].iloc[i:i+window].min()
#     if stock_prices['low'].iloc[i] <= potential_support * (1 + threshold):
#         if next_window_min >= potential_support * (1 - threshold):
#             support_levels.append((stock_prices['date'].iloc[i], potential_support))
             


# plt.figure(figsize=(12, 6))
# plt.plot(stock_prices['date'],stock_prices['close'], label='Close Price')
# support_levels = pd.stock_pricesFrame(support_levels,columns= ['date','support_level'])
# print(support_levels)
# # plt.plot(x=0,y=support_levels['support_level'], color='green', linestyle='--')
# plt.axhline(y=support_levels['support_level'].mean(),color='blue')
# plt.axhline(y=support_levels['support_level'].median(),color='red')
# # plt.axhline(y=support_levels['support_level'].mode(),color='yellow')
# # for level in support_levels:
# plt.plot(support_levels['date'],support_levels['support_level'], color='green')  # Green circles for support

# # for level in resistance:
# #     plt.plot(level[0], level[1], 'ro')  # Red circles for resistance

# # plt.plot(support, label='Support Line', color='green', linestyle='--')
# # plt.plot(resistance, label='Resistance Line', color='red', linestyle='--')
# # plt.title(f'{ticker} Support and Resistance Levels')
# plt.xlabel('date')
# plt.ylabel('Price')
# plt.legend()
# plt.ioff()
# plt.show()
# # plt.savefig()



# # except Exception as e:
# #     print(f"Error fetching stock_prices: {e}")
# #     # return []

import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
# Create a stock_pricesFrame to represent opening, closing, high, and low prices
# of a stock for a week
# stock_prices = pd.DFrame({'open': [60, 70, 80, 90, 100, 110, 120],
#    'close': [55, 85, 75, 100, 95, 120, 105],
#    'high': [70, 95, 85, 110, 105, 120, 125],
#    'low': [50, 60, 70, 80, 85, 105, 100]},
#    index=pd.date_range("2023-04-01", periods=7, freq="d"))
stock_prices = pd.read_json("/home/nishant.barevadiya/Work/flask-fintech/response_2.json")
stock_prices = stock_prices[['open', 'high','low', 'close', 'volume', 'date']]
# stock_prices = stock_prices[stock_prices['date']>pd.Timestamp(2024,8,15,14,0,0)] 
# stock_prices = stock_prices[stock_prices['date']<pd.Timestamp(2024,8,15,15,0,0)]

# stock_prices = stock_prices.set_index('date')


plt.figure()

##################################33

support_level = stock_prices[stock_prices['low']== stock_prices['low'].rolling(window=5,center=True).min()]
resistance_level = stock_prices[stock_prices['high']== stock_prices['high'].rolling(window=5,center=True).max()]
print(support_level)
support_mean = stock_prices['low'].mean()
resistance_mean = stock_prices['high'].mean()
print(support_level[abs(support_level['low'].diff())>.500])


support_level = support_level[abs(support_level['low'].diff())>.100]
resistance_level = resistance_level[abs(resistance_level['high'].diff())>.100]

mean = np.mean(stock_prices['high']- stock_prices['low'])
support_level_mean = support_level[abs(support_level['low'].diff())>mean]
resistance_level_mean = resistance_level[abs(resistance_level['high'].diff())>mean]
print("support_mean")
print(support_level_mean, support_mean)

####################################

# Create a new stock_pricesFrame called "up" that stores the stock_prices
# when the closing stock price is greater than or equal to the opening stock price
up = stock_prices[stock_prices.close >= stock_prices.open]

# Create a new stock_pricesFrame called "down" that stores the stock_prices
# when the closing stock price is lesser than the opening stock price
down = stock_prices[stock_prices.close < stock_prices.open]
print(up,down)

width = 0.0002

plt.vlines(x=up.date, ymin=up["low"], ymax=up["high"],
           color="green")
plt.vlines(x=down.date, ymin=down["low"], ymax=down["high"],
           color="red")

##Green Candles
plt.bar(x=up.date,height=up["close"] - up["open"],width=width, bottom=up["open"], color='green')

##Red Candles
plt.bar(x=down.date,height=down["open"] - down["close"],width=width, bottom=down["close"],  color="red")



# Rotate the x-axis tick labels at 45 degrees towards right
plt.xticks(rotation=45, ha='right')

plt.hlines(support_level['low'],xmax=support_level['date'].shift(-1), xmin=support_level['date'], color='green', label="Support Line")
# plt.hlines(support_level_mean['low'],xmax=support_level_mean['date'].shift(-1), xmin=support_level_mean['date'], color='yellow', label="Support mean Line")

plt.hlines(resistance_level['high'],xmax=resistance_level['date'].shift(-1), xmin=resistance_level['date'], color='red', label="Resistance Line")
plt.figure()
plt.bar(x=stock_prices.index,height=stock_prices['volume'], width=0.0002)


##################################33
plt.figure()

##################################33

support_level = stock_prices[stock_prices['low']== stock_prices['low'].rolling(window=9,center=True).min()]
resistance_level = stock_prices[stock_prices['high']== stock_prices['high'].rolling(window=9,center=True).max()]
print(support_level)
support_mean = stock_prices['low'].mean()
resistance_mean = stock_prices['high'].mean()
print(support_level[abs(support_level['low'].diff())>.500])


support_level = support_level[abs(support_level['low'].diff())>.100]
resistance_level = resistance_level[abs(resistance_level['high'].diff())>.100]

mean = np.mean(stock_prices['high']- stock_prices['low'])
support_level_mean = support_level[abs(support_level['low'].diff())>mean]
resistance_level_mean = resistance_level[abs(resistance_level['high'].diff())>mean]
print("support_mean")
print(support_level_mean, support_mean)

####################################

# Create a new stock_pricesFrame called "up" that stores the stock_prices
# when the closing stock price is greater than or equal to the opening stock price
up = stock_prices[stock_prices.close >= stock_prices.open]

# Create a new stock_pricesFrame called "down" that stores the stock_prices
# when the closing stock price is lesser than the opening stock price
down = stock_prices[stock_prices.close < stock_prices.open]
print(up,down)

width = 0.0004

plt.vlines(x=up.date, ymin=up["low"], ymax=up["high"],
           color="green")
plt.vlines(x=down.date, ymin=down["low"], ymax=down["high"],
           color="red")

##Green Candles
plt.bar(x=up.date,height=up["close"] - up["open"],width=width, bottom=up["open"], color='green')

##Red Candles
plt.bar(x=down.date,height=down["open"] - down["close"],width=width, bottom=down["close"],  color="red")



# Rotate the x-axis tick labels at 45 degrees towards right
plt.xticks(rotation=45, ha='right')

# plt.hlines(support_level['low'],xmax=support_level['date'].shift(-1), xmin=support_level['date'], color='green', label="Support Line")
plt.hlines(support_level['low'],xmax=support_level['date'].shift(-1), xmin=support_level['date'], color='green', label="Support mean Line")

plt.hlines(resistance_level['high'],xmax=resistance_level['date'].shift(-1), xmin=resistance_level['date'], color='red', label="Resistance Line")
plt.figure()
plt.bar(x=stock_prices.index,height=stock_prices['volume'], width=0.0002)


# Display the candlestick chart of stock stock_prices for a week
plt.title('Stock Prices for a Week')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.show()