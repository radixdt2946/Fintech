# Fintech APIS

### API 1 : /quote [Get]
Fetch financial data.
Fetch the financial data for a given stock symbol.

#### Parameters:
Symbol: Any stock symbol. [String]
#### cURL:
```
http://127.0.0.1:8000/quote?symbol=<Add symbol here>
```

### API 2 : /patterns [Post]
Detect stock price patterns for a given stock symbol and pattern type.

#### cURL For DoubleTop:
```
curl --location --request POST 'http://127.0.0.1:8000/patterns' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"NVDA",
    "period":"1y",
    "timeframe":"1d",
    "pattern_type":{
        "type": "double_top",
        "similarity_threshold": 0.02
    }
}' 
```
#### cURL For Support:
```
curl --location --request POST 'http://127.0.0.1:8000/patterns' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"GOOG",
    "period":"1y",
    "timeframe":"1d",
    "investment":"10000",
    "pattern_type":{
        "type": "support",
        "window": 9,
        "similarity_difference": 0.1
    }
}' 
```
#### cURL For Resistance:
```
curl --location --request POST 'http://127.0.0.1:8000/patterns' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"GOOG",
    "period":"1y",
    "timeframe":"1d",
    "investment":"10000",
    "pattern_type":{
        "type": "resistance",
        "window": 9,
        "similarity_difference": 0.1
    }
}' 
```
### API 3 : /backtest [Post]
Perform a backtest for a given trading strategy.

We can use SMA/EMA crossover strategy for backtest to get single for buy or sell. To determine stoploss and target, we have used ATR(Average True Range), percentage and point. 
#### cURL For Backtesting with SMA and ATR
```
curl --location --request POST 'http://127.0.0.1:8000/backtest' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"NVDA",
    "period":"1y",
    "timeframe":"1d",
    "investment":10000,
    "indicator":{
        "strategy":"sma",
        "short_window":50,
        "long_window":200
    },
    "oco":{
        "strategy":"atr",
        "atr_multiplier":2,
        "atr_period":14
    }
}'
```

#### cURL For Backtesting with EMA and ATR
```
curl --location --request POST 'http://127.0.0.1:8000/backtest' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"NVDA",
    "period":"1y",
    "timeframe":"1d",
    "investment":10000,
    "indicator":{
        "strategy":"EMA",
        "short_window":50,
        "long_window":200,
        "multiplier": 2
    },
    "oco":{
        "strategy":"atr",
        "atr_multiplier":2,
        "atr_period":14
    }
}'
```

#### cURL For Backtesting with SMA and OCO Percent
```
curl --location --request POST 'http://127.0.0.1:8000/backtest' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"NVDA",
    "period":"1y",
    "timeframe":"1d",
    "investment":10000,
    "indicator":{
        "strategy":"sma",
        "short_window":50,
        "long_window":200
    },
    "oco":{
        "strategy":"percent",
        "percent_risk":2,
        "percent_reward":5
    }
}'
```

#### cURL For Backtesting with EMA and OCO Percent
```
curl --location --request POST 'http://127.0.0.1:8000/backtest' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"NVDA",
    "period":"1y",
    "timeframe":"1d",
    "investment":10000,
    "indicator":{
        "strategy":"EMA",
        "short_window":50,
        "long_window":200,
        "multiplier": 2
    },
    "oco":{
        "strategy":"percent",
        "percent_risk":2,
        "percent_reward":5
    }
}'
```

#### cURL For Backtesting with SMA and OCO Point
```
curl --location --request POST 'http://127.0.0.1:8000/backtest' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"NVDA",
    "period":"1y",
    "timeframe":"1d",
    "investment":10000,
    "indicator":{
        "strategy":"sma",
        "short_window":50,
        "long_window":200
    },
    "oco":{
        "strategy":"point",
        "percent_risk":2,
        "percent_reward":5
    }
}'
```

#### cURL For Backtesting with EMA and OCO Point
```
curl --location --request POST 'http://127.0.0.1:8000/backtest' \
--header 'Content-Type: application/json' \
--data-raw '{
    "symbol":"NVDA",
    "period":"1y",
    "timeframe":"1d",
    "investment":10000,
    "indicator":{
        "strategy":"EMA",
        "short_window":50,
        "long_window":200,
        "multiplier": 2
    },
    "oco":{
        "strategy":"point",
        "percent_risk":2,
        "percent_reward":5
    }
}'
```