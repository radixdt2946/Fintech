import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

ticker = 'GOOG'
ticker = 'NVDA'

# ticker = yf.Ticker(ticker)   
data = yf.download(ticker, period='1y', interval='1d')
data = data.reset_index()
print(data)
# data['Date'] = data['Datetime']#.dt.strftime('%Y-%m-%dT%H:%M:%S')
data = data[['Open', 'High',
                'Low', 'Close',
                'Volume', 'Date']]
data['symbol'] = ticker
# data.columns = data.columns.str.Lower()
# data = data.to_dict('records')
print("1")
# try:
    
# data = pd.read_json("/home/nishant.barevadiya/Work/flask-fintech/response_2.json")
# print(data)

data = data[['Open', 'High',
                'Low', 'Close', 'Volume', 'Date']]
# print(data[data['Date']==pd.Timestamp(2024,8,8)])
# data = data[data['Date']>pd.Timestamp(2024,1,1,12,0,0)]
data = data.reset_index()

# # window=15
# bottom_node = data[data['Low']== data['Low'].rolling(window=9,center= True).min()]
# # bottom_node = bottom_node[abs(bottom_node['Low'].diff())>.050]
# top_node = data[data['High']== data['High'].rolling(window=9, center=True).max()]
# # top_node = top_node[abs(top_node['High'].diff())>.03]

# top_node['old_index'] = top_node.index
# top_node = top_node.reset_index()
# index = []
# for i in range(len(top_node)-1):
#     print("for loop")

#     print((abs(top_node.iloc[i]['High'] - top_node.iloc[i+1]['High']) / top_node.iloc[i]['High']),">0.05")
#     if (abs(top_node.iloc[i]['High'] - top_node.iloc[i+1]['High']) / top_node.iloc[i]['High']) < 0.0003:
#         # print((abs(top_node.iloc[i]['High'] - top_node.iloc[i+1]['High']) / top_node.iloc[i]['High']))
#         print("if condition")
#         index.append(i)
# print(len(index))
# print(len(top_node)) 
# top_node=top_node.drop(index)     
# # top_node = top_node.drop(i)
# print("after remove",len(top_node)) 

# print(top_node)
# # for i, row in top_node.iterrows():
# #     if abs(top_node[i] - top_node[i+1]) / top_node[i] <= 0.03:
# #         # Check if the price falls beLow the trough after the second peak
# #         if top_node[(i+1) + 1:].min() < prices[j]:
# #             double_tops.append((i, j, k))
# #             break
# plt.figure(figsize=(12, 6))
# # plt.plot(data['Date'],data['Close'], label='Close Price')


# #################Plot#######################
# up = data[data.Close >= data.Open]
# down = data[data.Close < data.Open]

# width = 0.0002

# plt.vlines(x=up.Date, ymin=up["Low"], ymax=up["High"],
#            color="green")
# plt.vlines(x=down.Date, ymin=down["Low"], ymax=down["High"],
#            color="red")

# ##Green Candles
# plt.bar(x=up.Date,height=up["Close"] - up["Open"],width=width, bottom=up["Open"], color='green')

# ##Red Candles
# plt.bar(x=down.Date,height=down["Open"] - down["Close"],width=width, bottom=down["Close"],  color="red")

# # Rotate the x-axis tick labels at 45 degrees towards right
# plt.xticks(rotation=45, ha='right')

# for index,row in bottom_node.iterrows():
#     # print(i)
#     plt.plot(row['Date'],row['Low'], color='cyan',marker="o",)
# for index,row in top_node.iterrows():
#     # print(i)
#     plt.plot(row['Date'],row['High'], color='cyan',marker="o",)



# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.legend()
# plt.ioff()
# plt.show()
# # plt.savefig()

###############################################################
######################### Double Top ##########################
# Identify local maxima (peaks)
peaks, _ = find_peaks(data['Close'], distance=10)  # distance parameter controls how Close peaks can be

print(data)
# Filter peaks with minimum prominence to ensure they are significant
peaks, properties = find_peaks(data['Close'], prominence=1, distance=10)
print(peaks, properties)
data['Peak'] = None
print(data.iloc[peaks])

data.loc[peaks, 'Peak'] = data.iloc[peaks].Close

# Define a list to store detected double tops
double_tops = []

# Parameters for double top detection
similarity_threshold = 0.02  # 2% similarity between peaks

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
print(double_tops_df)

###############################################################
# Plot the stock price and Highlight the detected double tops
# plt.figure(figsize=(14, 7))
# plt.plot(data['Close'], label='Close Price')
# #################Plot#######################

plt.figure(figsize=(12, 6))

up = data[data.Close >= data.Open]
# Create a new dataFrame called "down" that stores the data
# when the closing stock price is lesser than the Opening stock price
down = data[data.Close < data.Open]

# width = 4

plt.vlines(x=up.Date, ymin=up["Low"], ymax=up["High"],
           color="green")
plt.vlines(x=down.Date, ymin=down["Low"], ymax=down["High"],
           color="red")

##Green Candles
plt.bar(x=up.Date,height=up["Close"] - up["Open"],bottom=up["Open"], color='green')

##Red Candles
plt.bar(x=down.Date,height=down["Open"] - down["Close"], bottom=down["Close"],  color="red")

for _, row in double_tops_df.iterrows():
    plt.plot([data['Date'].iloc[row['first_peak']], data['Date'].iloc[row['second_peak']]], 
             [data['Close'].iloc[row['first_peak']], data['Close'].iloc[row['second_peak']]], 
             'ro-', lw=2 )
    plt.plot(data['Date'].iloc[row['trough']], data['Close'].iloc[row['trough']], 'go', markersize=8)
    plt.plot(data['Date'].loc[row['breakdown']], data['Close'].iloc[row['breakdown']], 'bo', markersize=8 )

plt.title('Double Top Pattern Detection')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
