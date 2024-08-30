# Fintech APIS
### Index:
1. Steps for installation
2. API's
3. To-do's


## Steps for Installation:
1. Create Python Virtual Environment in your folder
```bash
python3 -m venv .<venv-name>
```

2. Activate the virtual environment in the terminal

For MacOS/Linux
```bash
source .<venv-name>/bin/activate
```
For Windows
```powershell
.<venv-name>\Scripts\activate.bat
```

3. Install all the requirements present in requirements.txt

```bash
pip install --upgrade -r requirements.txt
```
To run the flask app you can execute

```bash
flask run
```

## APIs

#### API 1 : /quote [Get]
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


## To-Dos
##### 1. Integrate Docker: 
Implement Docker support for easier deployment and containerization.
This may involve:
1. Creating a Dockerfile that defines the project environment and dependencies.
2. Building and running Docker images for development and production.
3. Updating project documentation to reflect Docker usage.

##### 2.Code Optimization: 
Improve code performance and efficiency.
This could involve:
1. Utilize profiling tools to identify performance bottlenecks within the application.
2. Refactoring code for better readability, maintainability and potential optimization opportunities.
3. Explore and implement optimization techniques such as caching, memoization, and algorithmic improvements to enhance code efficiency.

##### 3. Add Celery Functionality: 
Implement Celery for asynchronous tasks and background processing.
This includes:
1. Installing and configuring Celery.
2. Defining tasks for background processing.
3. Integrating Celery with your existing application logic.




