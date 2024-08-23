import yfinance as yf
# from app.models import StockData
import pandas as pd
ticker = 'AAPL'
import numpy as np

import matplotlib.pyplot as plt
print("1")
# try:
    
data = pd.read_json("/home/nishant.barevadiya/Work/flask-fintech/response_2.json")
print(data)

data = data.reset_index()
data = data[['open', 'high',
                'low', 'close', 'volume', 'date']]
print(data.describe())
data.dropna(inplace=True)  # Remove rows with missing values

# print(data[data['date']==pd.Timestamp(2024,8,8)])
# data = data[data['date']>pd.Timestamp(2024,8,15,12,0,0)]
# window=15




## SMA calculation
data['SMA10'] = data['close'].rolling(window=10,min_periods=1).mean()
data['SMA20'] = data['close'].rolling(window=50,min_periods=1).mean()

# EMA Calculation
# number of observations = exmple (10,20,..)
# multiplier = [2 ÷ (number of observations + 1)]
#EMA = Closing price x multiplier + EMA (previous day) x (1-multiplier)

multiplier = 2 / (10 +1)
print(multiplier)
data['EMA'] = None

for i in range(10,len(data)):
    if i == 10:
        # data.loc[i,'EMA'] = data.iloc[i]['SMA20']
        print(data.iloc[:i]['close'])
        data.loc[i,'EMA'] = (data.iloc[:i]['close'].sum())/10
    else:
        # pass
        data.loc[i,'EMA'] = data.iloc[i]['close'] * multiplier + data.iloc[i-1]['EMA'] * (1 - multiplier)
print(data.iloc[11])


#######################################################################################################################################
#####################################   Simulation    ################################

def simple_moving_average_strategy(data, short_window=50, long_window=200):
    """A simple moving average crossover strategy."""

    short_sma = data['close'].rolling(window=short_window, min_periods=1).mean()
    long_sma = data['close'].rolling(window=long_window, min_periods =1).mean()

    buy_signals = (short_sma > long_sma) & (data['close'] > long_sma)
    sell_signals = (short_sma < long_sma) & (data['close'] < long_sma)

    return buy_signals, sell_signals

buy_signals, sell_signals = simple_moving_average_strategy(data, 10, 50)
print("buy_signal",sum(x for x in buy_signals if x))
print("sell_signal",sum(x for x in sell_signals if x))
print("sell_signal",sum(x for x in (sell_signals & buy_signals) if x))
# Initialize variables
position = 0
initial_investment = 10000
portfolio_value = initial_investment
returns = []

investment = pd.DataFrame()

# ... (rest of your backtesting code)


atr_multiplier=2
atr_period = 14

data['TR'] = abs(data['high'] - data['low'])
data['TR1'] = abs(data['high'] - data['close'].shift(1))
data['TR2'] = abs(data['low'] - data['close'].shift(1))
data['True_Range'] = data[['TR', 'TR1', 'TR2']].max(axis=1)
data['ATR'] = data['True_Range'].rolling(window=14, min_periods=1).mean()

atr= data['ATR']
# atr = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=atr_period)
stop_loss = 0
target = 0
buy_tracker = pd.DataFrame()
sell_tracker = pd.DataFrame()
for index, row in data.iterrows():
    if position == 0 and buy_signals[index]:
        position = initial_investment / row['close']
        entry_price = row['close']
        stop_loss = entry_price - atr[index] * atr_multiplier
        target = entry_price + atr[index] * atr_multiplier
        print("Buy:",position,"initial incest",initial_investment," investment:",(position * row['close'])," portfolio value:", portfolio_value)
        buy_tracker=buy_tracker._append({'date':row['date'], 'price':row['close']},ignore_index=True)
    elif (row['low'] <= stop_loss or row['high'] >= target) and position > 0 : #and sell_signals[index]:
        portfolio_value = position * row['close']
        exit_price = row['close']
        profit = exit_price - entry_price
        risk = entry_price - stop_loss

        invest_dict = {"investment": initial_investment,
            'position' : position,
            'returns' : (portfolio_value / initial_investment - 1),
            'sell_value' : portfolio_value,
            'Profit/Loss' : portfolio_value - initial_investment,
            'risk' : risk,
            'top_loss': stop_loss,
            'target' : target,
            'entry_price': entry_price,
            'exit_price': exit_price,
        }
        investment = investment._append(invest_dict, ignore_index = True)
        
        position = 0
        returns.append(portfolio_value / initial_investment - 1)
        
        print("sell:",portfolio_value, " returns:",(portfolio_value / initial_investment - 1))
        sell_tracker=sell_tracker._append({'date':row['date'], 'price':row['close']},ignore_index=True)

print(investment)
# for index, row in data.iterrows():
#     if position == 0 and buy_signals[index]:
#         position = np.floor(portfolio_value / row['close'])
#         portfolio_value = portfolio_value % row['close']
#         print("Buy:",position," investment:",(position * row['close'])," portfolio value:", portfolio_value)
#     elif position > 0 and sell_signals[index]:
#         sell_value = position * row['close']
#         position = 0
#         returns.append(sell_value / initial_investment - 1)
#         portfolio_value += sell_value
#         print("sell:",sell_value," portfolio value:", portfolio_value, " returns:",(sell_value / initial_investment - 1))

# Calculate final portfolio value
portfolio_value += position * data['close'].iloc[-1]
print("portfolio:",portfolio_value)

data1 = data[buy_signals | sell_signals]
# print(buy_signals | sell_signals)
# print(data1,data1.index)
returns = pd.Series(returns)
# print(1+returns,"||",returns)

cumulative_returns = (1 + returns).cumprod()

# Calculate performance metrics
annualized_return = cumulative_returns.iloc[-1] ** (252 / len(returns)) - 1
sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)

print("Annualized Return:", annualized_return)
print("Sharpe Ratio:", sharpe_ratio)

num_winning_trades = len(returns[returns > 0])
num_losing_trades = len(returns[returns < 0])
profit_loss = portfolio_value - initial_investment
average_risk_reward = returns.mean() / abs(returns[returns < 0].mean())

# Print the results
print("Profit/Loss:", profit_loss)
print("Number of Winning Trades:", num_winning_trades)
print("Number of Losing Trades:", num_losing_trades)
print("Average Risk/Reward Ratio:", average_risk_reward)
print("reverse:",abs(returns[returns < 0].mean()) / returns.mean())
# ... (rest of the code remains the same)

def calculate_average_rr(trades):
    
    # return sum(abs(trade['profit']) for trade in losing_trades) / len(losing_trades)
    # return abs(trades[trades < 0]).mean()/ trades[trades > 0].mean() 
    print(trades[trades > 0].mean() / trades[trades < 0].mean()*-1 )
    return trades[trades < 0].mean()*-1 / trades[trades > 0].mean() 
#   winning_trades = [trade for trade in trades if trade['profit'] > 0]
#   losing_trades = [trade for trade in trades if trade['profit'] < 0]

#   if len(winning_trades) == 0 or len(losing_trades) == 0:
#     return 0  # Avoid division by zero

#   average_profit = sum(trade['profit'] for trade in winning_trades) / len(winning_trades)
#   average_loss = sum(abs(trade['profit']) for trade in losing_trades) / len(losing_trades)




print("Cumulative Profit/Loss:", sum(investment['Profit/Loss']))
print("Average RR:", calculate_average_rr(investment['Profit/Loss']))


print("toploss and target average RR :",sum(investment['risk'])/len(investment['risk']))
print("final:",np.mean(investment['entry_price'] - investment['top_loss'] / investment['target'] - investment['entry_price']))







plt.figure(figsize=(12, 6))

up = data[data.close >= data.open]
# Create a new dataFrame called "down" that stores the data
# when the closing stock price is lesser than the opening stock price
down = data[data.close < data.open]

width = 0.0004

plt.vlines(x=up.date, ymin=up["low"], ymax=up["high"],
           color="green")
plt.vlines(x=down.date, ymin=down["low"], ymax=down["high"],
           color="red")

##Green Candles
plt.bar(x=up.date,height=up["close"] - up["open"],width=width, bottom=up["open"], color='green')

##Red Candles
plt.bar(x=down.date,height=down["open"] - down["close"],width=width, bottom=down["close"],  color="red")


# Plot SMA in graph
plt.plot(data['date'],data['SMA10'], label= 'SMA10', color='yellow')
plt.plot(data['date'],data['SMA20'], label= 'SMA50', color='cyan')
# plt.plot(data['date'],data['EMA'], label='EMA', color = 'tomato')
plt.plot(data[buy_signals]['date'],data[buy_signals]['close'])
plt.plot(data[sell_signals]['date'],data[sell_signals]['close'])
# Plot the results
plt.plot(buy_tracker['date'],buy_tracker['price'], 'o:g')
plt.plot(sell_tracker['date'],sell_tracker['price'], 'o:r')
# plt.plot(cumulative_returns)



plt.xlabel('date')
plt.ylabel('Price')
plt.legend()
plt.ioff()

plt.figure()


# Plot the results
plt.plot(cumulative_returns)
plt.title("Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Returns")


plt.show()
# plt.savefig()



