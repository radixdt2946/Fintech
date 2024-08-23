import yfinance as yf
# from app.models import StockData
import pandas as pd
ticker = 'AAPL'


import matplotlib.pyplot as plt
print("1")
# try:
    
data = pd.read_json("/home/nishant.barevadiya/Work/flask-fintech/response_2.json")
# print(data)

data = data.reset_index()
data = data[['open', 'high',
                'low', 'close', 'volume', 'date']]
# print(data[data['date']==pd.Timestamp(2024,8,8)])
data = data[data['date']>pd.Timestamp(2024,8,15,12,0,0)]
# window=15
bottom_node = data[data['low']== data['low'].rolling(window=9,center= True).min()]
# bottom_node = bottom_node[abs(bottom_node['low'].diff())>.050]
top_node = data[data['high']== data['high'].rolling(window=9, center=True).max()]
# top_node = top_node[abs(top_node['high'].diff())>.03]

top_node['old_index'] = top_node.index
top_node = top_node.reset_index()
index = []
for i in range(len(top_node)-1):
    print("for loop")

    print((abs(top_node.iloc[i]['high'] - top_node.iloc[i+1]['high']) / top_node.iloc[i]['high']),">0.05")
    if (abs(top_node.iloc[i]['high'] - top_node.iloc[i+1]['high']) / top_node.iloc[i]['high']) < 0.0003:
        # print((abs(top_node.iloc[i]['high'] - top_node.iloc[i+1]['high']) / top_node.iloc[i]['high']))
        print("if condition")
        index.append(i)
print(len(index))
print(len(top_node)) 
top_node=top_node.drop(index)     
# top_node = top_node.drop(i)
print("after remove",len(top_node)) 

print(top_node)
# for i, row in top_node.iterrows():
#     if abs(top_node[i] - top_node[i+1]) / top_node[i] <= 0.03:
#         # Check if the price falls below the trough after the second peak
#         if top_node[(i+1) + 1:].min() < prices[j]:
#             double_tops.append((i, j, k))
#             break
plt.figure(figsize=(12, 6))
# plt.plot(data['date'],data['close'], label='Close Price')


#################Plot#######################
up = data[data.close >= data.open]
down = data[data.close < data.open]

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

for index,row in bottom_node.iterrows():
    # print(i)
    plt.plot(row['date'],row['low'], color='cyan',marker="o",)
for index,row in top_node.iterrows():
    # print(i)
    plt.plot(row['date'],row['high'], color='cyan',marker="o",)



plt.xlabel('date')
plt.ylabel('Price')
plt.legend()
plt.ioff()
plt.show()
# plt.savefig()



