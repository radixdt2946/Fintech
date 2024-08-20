import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate some synthetic stock data (you can replace this with real stock data)
dates = pd.date_range('2023-01-01', periods=100)
prices = np.sin(np.linspace(0, 10, 100)) * 10 + 100 + np.random.normal(0, 1, 100)

df = pd.DataFrame({'Date': dates, 'Price': prices})

# Plotting the stock prices
plt.figure(figsize=(14, 8))
plt.plot(df['Date'], df['Price'], label='Stock Price')

# 1. Double Top Detection
df['Peak'] = df['Price'][(df['Price'].shift(1) < df['Price']) & (df['Price'].shift(-1) < df['Price'])]
peaks = df.dropna(subset=['Peak'])

if len(peaks) >= 2:
    # Assume Double Top if two peaks are within a small price range
    for i in range(len(peaks) - 1):
        if abs(peaks.iloc[i]['Peak'] - peaks.iloc[i + 1]['Peak']) < 1:
            plt.scatter([peaks.iloc[i]['Date'], peaks.iloc[i + 1]['Date']], 
                        [peaks.iloc[i]['Peak'], peaks.iloc[i + 1]['Peak']], color='red', label='Double Top')

# 2. Support Line
support_price = df['Price'].min()
plt.axhline(y=support_price, color='green', linestyle='-', label='Support Line')

# 3. Resistance Line
resistance_price = df['Price'].max()
plt.axhline(y=resistance_price, color='red', linestyle='-', label='Resistance Line')

# Customize and show plot
plt.title('Stock Price with Double Top, Support, and Resistance')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='best')
plt.show()
