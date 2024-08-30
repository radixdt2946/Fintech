import yfinance as yf
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Default constants
DEFAULT_SHORT_WINDOW = 50
DEFAULT_LONG_WINDOW = 200
DEFAULT_MULTIPLIER = 2
DEFAULT_INVESTMENT = 10000
DEFAULT_ATR_MULTIPLIER = 2
DEFAULT_ATR_PERIOD = 14

def fetch_stock_data(symbol: str, period: str = '1y', interval: str = '1d') -> pd.DataFrame:
    """
    Fetch stock data using yfinance.
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval).reset_index()
        return data.dropna(subset=['Close']) # Ensuring there are no missing 'Close' values
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()


def simple_moving_average_strategy(data : pd.DataFrame, short_window: int, long_window: int) -> (pd.Series, pd.Series):
    """
        Calculate moving average crossover strategy signals.

        Parameters:
        -----------
        data : pd.DataFrame
            A DataFrame containing stock price data with a 'Close' column.
        short_window : int, optional
            The window size for the short-term moving average (default is 50).
        long_window : int, optional
            The window size for the long-term moving average (default is 200).
    """
    try:
        short_sma = data['Close'].rolling(window=short_window).mean()
        long_sma = data['Close'].rolling(window=long_window).mean()

        buy_signals = (short_sma > long_sma) & (data['Close'] > long_sma)
        sell_signals = (short_sma < long_sma) & (data['Close'] < long_sma)

        return buy_signals, sell_signals
    except Exception as e:
        logger.error(f"Error in simple_moving_average_strategy: {e}")
        return pd.Series([False]* len(data)), pd.Series([False]* len(data))

def exponential_moving_average_strategy( data: pd.DataFrame, short_window: int, long_window: int, multiplier: float) -> (pd.Series, pd.Series):
    '''
        Calculate exponential moving average crossover strategy signals.

        Parameters:
        -----------
        data : pd.DataFrame
            A DataFrame containing stock price data with a 'Close' column.
        short_window : int
            The window size for the short-term EMA.
        long_window : int
            The window size for the long-term EMA.
    '''
    try:
        short_multiplier = multiplier / (short_window +1)
        long_multiplier = multiplier / (long_window +1)
        
        data['EMA_short'] = 0
        
        for i in range(short_window,len(data)):
        
            if i == short_window:
                data.loc[i,'EMA_short'] = (data.iloc[:i]['Close'].sum())/short_window
            else:
                data.loc[i,'EMA_short'] = data.iloc[i]['Close'] * short_multiplier + data.iloc[i-1]['EMA_short'] * (1 - short_multiplier)
        
        data['EMA_long'] = 0
        
        for i in range(long_window,len(data)):
            if i == long_window:
                data.loc[i,'EMA_long'] = (data.iloc[:i]['Close'].sum())/long_window
            else:
                data.loc[i,'EMA_long'] = data.iloc[i]['Close'] * long_multiplier + data.iloc[i-1]['EMA_long'] * (1 - long_multiplier)

        buy_signals = (data['EMA_short'] >  data['EMA_long']) & (data['Close'] >  data['EMA_long'])

        sell_signals = (data['EMA_short'] <  data['EMA_long']) & (data['Close'] <  data['EMA_long'])

        return buy_signals, sell_signals
    
    except Exception as e:
        logger.error(f"Error in exponential_moving_average_strategy: {e}")
        return pd.Series([False] * len(data)), pd.Series([False] * len(data))

def oco_ATR(data: pd.DataFrame, initial_investment: float, buy_signals: pd.Series, sell_signals: pd.Series, atr_multiplier: float, atr_period: int) -> pd.DataFrame:
    
    '''
        A one-cancels-other (OCO) trading strategy based on Average True Range (ATR).

        Parameters:
        -----------
        data : pd.DataFrame
            A DataFrame containing stock price data with 'High', 'Low', 'Close', and 'Volume' columns.
        initial_investment : float
            The amount of initial investment.
        buy_signals : pd.Series
            A boolean Series indicating buy signals.
        sell_signals : pd.Series
            A boolean Series indicating sell signals.
        atr_multiplier : float
            The multiplier for ATR to determine stop loss and take profit levels.
        atr_period : int
            The period for calculating the ATR.

        Returns:
        --------
        pd.DataFrame
            A DataFrame containing the investment report for each trade.
    '''
    try:

        investment_report = pd.DataFrame()

        data['TR'] = abs(data['High'] - data['Low'])
        data['TR1'] = abs(data['High'] - data['Close'].shift(1))
        data['TR2'] = abs(data['Low'] - data['Close'].shift(1))
        data['True_Range'] = data[['TR', 'TR1', 'TR2']].max(axis=1)
        data['ATR'] = data['True_Range'].rolling(window=atr_period, min_periods=1).mean()

        atr= data['ATR']
        stop_loss = 0
        target = 0
        position = 0
        
        for index, row in data.iterrows():
            if position == 0 and buy_signals[index]:
                position = initial_investment / row['Close']
                entry_price = row['Close']
                stop_loss = entry_price - atr[index] * atr_multiplier
                target = entry_price + atr[index] * atr_multiplier
            
            elif (row['Low'] <= stop_loss or row['High'] >= target) and position > 0 : #and sell_signals[index]:
                portfolio_value = position * row['Close']
                exit_price = row['Close']
                # profit = exit_price - entry_price
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
                investment_report = investment_report._append(invest_dict, ignore_index = True)
                
                position = 0
            
        return investment_report
    
    except Exception as e:
        logger.error(f"Error in oco_ATR: {e}")
        return pd.DataFrame()

def oco_percent_point(data: pd.DataFrame, initial_investment: float,buy_signals: pd.Series, risk: float, reward: float, use_percentage: bool) -> pd.DataFrame:
    
    '''
        A one-cancels-other (OCO) trading strategy based on fixed percentage or points.

        Parameters:
        -----------
        data : pd.DataFrame
            A DataFrame containing stock price data with 'High', 'Low', 'Close', and 'Volume' columns.
        initial_investment : float
            The amount of initial investment.
        buy_signals : pd.Series
            A boolean Series indicating buy signals.
        risk : float
            The risk level in percentage or points.
        reward : float
            The reward level in percentage or points.
        use_percentage : bool
            If True, uses percentage for stop loss and take profit levels; otherwise uses points.

        Returns:
        --------
        pd.DataFrame
            A DataFrame containing the investment report for each trade.
        
    '''

    try:

        investment_report = pd.DataFrame()

        stop_loss = 0
        target = 0
        position = 0


        # return stop_loss_price, take_profit_price

        for index, row in data.iterrows():
            if position == 0 and buy_signals[index]:
                position = initial_investment / row['Close']
                entry_price = row['Close']
                     
                if use_percentage:
                    stop_loss = entry_price * (1 - risk / 100)  # For long position
                    target = entry_price * (1 + reward / 100)  # For long position
                    
                else:
                    stop_loss = entry_price - risk
                    target = entry_price + reward

            elif (row['Low'] <= stop_loss or row['High'] >= target) and position > 0 : #and sell_signals[index]:
                portfolio_value = position * row['Close']
                exit_price = row['Close']
                # profit = exit_price - entry_price
                risk = entry_price - stop_loss

                invest_dict = {"investment": initial_investment,
                    'position' : position,
                    'returns' : (portfolio_value / initial_investment - 1),
                    'sell_value' : portfolio_value,
                    'Profit/Loss' : portfolio_value - initial_investment,
                    'risk' : risk,
                    'stop_loss': stop_loss,
                    'target' : target,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                }
                investment_report = investment_report._append(invest_dict, ignore_index = True)
                
                position = 0
            
        return investment_report
    
    except Exception as e:
        logger.error(f"Error in oco_percent_point: {e}")
        return pd.DataFrame()

def perform_backtest(strategy: dict) -> dict:
    '''
            Perform a trading backtest based on a provided strategy object.
    '''

    try:
        symbol = strategy['symbol']
        timeframe = strategy.get('timeframe', '1d')
        period = strategy.get('period','1y')
        ticker = yf.Ticker(symbol)    

        # it check that given ticker symbol is valid or not
        info = ticker.info
        if not info and 'regularMarketPrice' in info:
            return {"error":f'{symbol} is not a valid ticker symbol.',}
        
        data = ticker.history(period=period, interval=timeframe)


        data = data.reset_index()
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


        # Implement backtest logic based on the strategy provided  
        investment = strategy.get('investment','10000')

        position = 0
        initial_investment = investment
        portfolio_value = initial_investment
        investment_report = []

        indicator = strategy.get('indicator')
        oco = strategy.get('oco')

        
        if indicator:
            short_window = indicator.get('short_window',50)
            long_window = indicator.get('long_window',200)
            
            if str(indicator.get('strategy')).lower() == 'sma':
                buy_signals, sell_signals = simple_moving_average_strategy(data,short_window=short_window, long_window=long_window)

            elif str(indicator.get('strategy')).lower() == "ema":    
                multiplier = indicator.get('multiplier', 2)
                buy_signals, sell_signals = exponential_moving_average_strategy(data,short_window=short_window, long_window=long_window, multiplier=multiplier)

            else:
                return  {"error":"Invalid indicators"}


        if oco:
            oco_strategy = oco.get('strategy')
            if oco_strategy.lower()  == 'atr':

                atr_multiplier = oco.get('atr_multiplier',2)
                atr_period = oco.get('atr_period',14)

                investment_report = oco_ATR(data, initial_investment, buy_signals, sell_signals, atr_multiplier, atr_period)
            elif oco_strategy.lower() == 'percent':

                # Set Stop Loss and Take Profit using fixed percentage or points
                percent_risk = oco.get('percent_risk',2)
                percent_reward = oco.get('percent_reward',5)
                
                investment_report = oco_percent_point( data, initial_investment, buy_signals, percent_risk, percent_reward, use_percentage= True)
    
            elif oco_strategy.lower() == 'point':

                # Set Stop Loss and Take Profit using fixed percentage or points
                point_risk = oco.get('point_risk',5)
                point_reward = oco.get('point_reward',10)

                investment_report = oco_percent_point( data, initial_investment, buy_signals, point_risk, point_reward, use_percentage= False)

            else:
                return {"error": "Invalid OCO strategy"}

        else:
            # Logic for when no OCO strategy is provided

            for index, row in data.iterrows():
                if position == 0 and buy_signals[index]:
                    position = initial_investment / row['Close']

                elif position > 0 and sell_signals[index]:

                    portfolio_value = position * row['Close']
                    returns = portfolio_value / initial_investment - 1
                    profit_loss = portfolio_value - initial_investment

                    
                    invest_dict = {"investment": initial_investment,
                    'position' : position,
                    'returns' :returns,
                    'sell_value' : portfolio_value,
                    'Profit/Loss' : profit_loss}
                    investment_report = investment_report._append(invest_dict, ignore_index = True)
                    
                    position = 0


        cumulative_PL= round(sum(investment_report['Profit/Loss']),2)
        win_trades = sum(investment_report['Profit/Loss']>0)
        loss_trades = sum(investment_report['Profit/Loss']<0)

        average_rr =  0 
        if oco:
            
            investment_report['reward']=  (investment_report['target'] - investment_report['entry_price'])
            investment_report['RR_ratio'] = investment_report['reward'] / investment_report['risk']
            
            # Drop rows where RR_ratio is None (invalid trades)
            valid_rr = investment_report['RR_ratio'].dropna()
            
            average_rr = round(valid_rr.mean(),2)
        else:
            trades = investment_report['Profit/Loss']
            average_rr = round(trades[trades < 0].mean()*-1 / trades[trades > 0].mean(),2)

        result = {        
            'P&L': cumulative_PL,
            'winning_trades': win_trades,
            'losing_trades': loss_trades,
            'average_rr': average_rr,
        }

        return result

    except Exception as e:
        logger.error(f"Error in perform_backtest: {e}")
        return {"error": str(e)}