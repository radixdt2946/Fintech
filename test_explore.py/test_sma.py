import yfinance as yf
# from app.models import StockData
import pandas as pd
ticker = 'AAPL'


import matplotlib.pyplot as plt
print("1")
# try:
    
data = pd.read_json("/home/nishant.barevadiya/Work/flask-fintech/response_2.json")
print(data)

data = data.reset_index()
data = data[['open', 'high',
                'low', 'close', 'volume', 'date']]
print(data.describe())
# print(data[data['date']==pd.Timestamp(2024,8,8)])
# data = data[data['date']>pd.Timestamp(2024,8,15,12,0,0)]
# window=15

data['SMA10'] = data['close'].rolling(window=10).mean()
data['SMA20'] = data['close'].rolling(window=20).mean()

plt.figure(figsize=(12, 6))
plt.plot(data['date'],data['close'], label='Close Price')
plt.plot(data['date'],data['SMA10'], label= 'SMA10', color='yellow')
plt.plot(data['date'],data['SMA20'], label= 'SMA20', color='cyan')



print(data[20:])



plt.xlabel('date')
plt.ylabel('Price')
plt.legend()
plt.ioff()
plt.show()
# plt.savefig()



