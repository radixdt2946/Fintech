import yfinance as yf
import pandas as pd

def simple_moving_average_strategy(data, short_window=50, long_window=200):
    """A simple moving average crossover strategy."""

    short_sma = data['close'].rolling(window=short_window).mean()
    long_sma = data['close'].rolling(window=long_window).mean()

    buy_signals = (short_sma > long_sma)#& (data['close'] > long_sma)
    sell_signals = (short_sma < long_sma) #& (data['close'] < long_sma)

    return buy_signals, sell_signals



def perform_backtest(strategy):
    symbol = strategy['symbol']
    timeframe = strategy.get('timeframe', '1d')
    ticker = yf.Ticker(symbol)    
    data = ticker.history(period="5y", interval=timeframe)

    # Implement backtest logic based on the strategy provided  
    
    position = 0
    initial_investment = 10000
    portfolio_value = initial_investment
    returns = []

    buy_signals, sell_signals = simple_moving_average_strategy(data,short_window=50, long_window=200)

    investment = pd.DataFrame()

    for index, row in data.iterrows():
        if position == 0 and buy_signals[index]:
            position = initial_investment / row['close']
            # print("Buy:",position,"initial incest",initial_investment," investment:",(position * row['close'])," portfolio value:", portfolio_value)

        elif position > 0 and sell_signals[index]:
            portfolio_value = position * row['close']
            invest_dict = {"investment": initial_investment,
            'position' : position,
            'returns' : (portfolio_value / initial_investment - 1),
            'sell_value' : portfolio_value,
            'Profit/Loss' : portfolio_value - initial_investment}
            investment = investment._append(invest_dict, ignore_index = True)
            
            position = 0
            returns.append(portfolio_value / initial_investment - 1)            
            # print("sell:",portfolio_value, " returns:",(portfolio_value / initial_investment - 1))

    # print(investment)

    cumulative_PL= sum(investment['Profit/Loss'])
    win_trades = sum(investment['Profit/Loss']>0)
    loss_trades = sum(investment['Profit/Loss']<0)
    result = {        
        'P/L': cumulative_PL,
        'winning_trades': win_trades,
        'losing_trades': loss_trades,
        'average_rr': 0,
    }

    return result