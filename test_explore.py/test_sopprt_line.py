import yfinance as yf
# from app.models import StockData
import pandas as pd

import matplotlib.pyplot as plt 
from mpl_finance import candlestick_ohlc 
import pandas as pd 
import matplotlib.dates as mpl_dates 
import numpy as np 
import datetime

ticker = 'AAPL'


import matplotlib.pyplot as plt
print("1")
# try:
    
data = pd.read_json("/home/nishant.barevadiya/Work/flask-fintech/response_2.json")
print(data)

data = data.reset_index()
data['date'] = pd.to_datetime(data['date']) 

data['date'] = data['date'].apply(mpl_dates.date2num) 




data = data[['open', 'high',
                'low', 'close', 'volume', 'date']]
data = data.astype(float) 

print(data.describe())
# print(data[data['date']==pd.Timestamp(2024,8,8)])
# data = data[data['date']>pd.Timestamp(2024,8,15,12,0,0)]
# window=15

support_level = data[data['low']== data['low'].rolling(window=5,center=True).min()]
resistance_level = data[data['high']== data['high'].rolling(window=5,center=True).max()]
print(support_level)

print(support_level[abs(support_level['low'].diff())>.500])

support_level = support_level[abs(support_level['low'].diff())>.100]
resistance_level = resistance_level[abs(resistance_level['high'].diff())>.100]

data['shift_date']=data['date'].shift(1)
print(data)
max_date= data['date'].max()

fig, ax = plt.subplots() 

candlestick_ohlc(ax, data.values, width=0.6, colorup='blue', 
				colordown='green', alpha=0.4) 

plt.figure(figsize=(12, 6))
# plt.plot(data['date'],data['close'], label='Close Price')
# for i in support_level:
# plt.plot(data['date'],data['low'], label='Close Price', color='blue')
# plt.plot(data['date'],data['high'], label='Close Price', color='orange')
plt.hlines(support_level['low'],xmax=support_level['date'].shift(-1), xmin=support_level['date'], color='green', label="Support Line")
plt.hlines(resistance_level['high'],xmax=resistance_level['date'].shift(-1), xmin=resistance_level['date'], color='red', label="Resistance Line")


# Setting labels & titles 
ax.set_xlabel('Date') 
ax.set_ylabel('Price') 
fig.suptitle('Stock Prices of a week') 

# Formatting Date 
date_format = mpl_dates.DateFormatter('%d-%m-%Y') 
ax.xaxis.set_major_formatter(date_format) 
fig.autofmt_xdate() 

fig.tight_layout() 

plt.show() 


# plt.xlabel('date')
# plt.ylabel('Price')
# plt.legend()
# plt.ioff()
# plt.show()
# # plt.savefig()



# # Importing all the required libraries 

# import matplotlib.pyplot as plt 
# from mpl_finance import candlestick_ohlc 
# import pandas as pd 
# import matplotlib.dates as mpl_dates 
# import numpy as np 
# import datetime 


# # Defining a dataframe showing stock prices 
# # of a week 
# stock_prices = pd.DataFrame({'date': np.array([datetime.datetime(2021, 11, i+1) 
# 											for i in range(7)]), 
# 							'open': [36, 56, 45, 29, 65, 66, 67], 
# 							'close': [29, 72, 11, 4, 23, 68, 45], 
# 							'high': [42, 73, 61, 62, 73, 56, 55], 
# 							'low': [22, 11, 10, 2, 13, 24, 25]}) 

# ohlc = stock_prices.loc[:, ['date', 'open', 'high', 'low', 'close']] 
# ohlc['date'] = pd.to_datetime(ohlc['date']) 
# ohlc['date'] = ohlc['date'].apply(mpl_dates.date2num) 
# ohlc = ohlc.astype(float) 

# # Creating Subplots 
# fig, ax = plt.subplots() 

# candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='blue', 
# 				colordown='green', alpha=0.4) 

# # Setting labels & titles 
# ax.set_xlabel('Date') 
# ax.set_ylabel('Price') 
# fig.suptitle('Stock Prices of a week') 

# # Formatting Date 
# date_format = mpl_dates.DateFormatter('%d-%m-%Y') 
# ax.xaxis.set_major_formatter(date_format) 
# fig.autofmt_xdate() 

# fig.tight_layout() 

# plt.show() 


