import pytest

def test_backtest(client):

    input_json = {
            "symbol":"GOOG",
            "period":"1y",
            "timeframe":"1d",
            "investment":"10000",
            "indicator":{
                "strategy":"sma",
                "short_window":50,
                "long_window":200,
            },
            "oco":{
                "strategy":"atr",
                "atr_multiplier":2,
                "atr_period":14
            }
        }
    response = client.post('/backtest', json=input_json)
    assert response.status_code == 200