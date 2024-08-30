import pytest

def test_patterns(client):

    json_input = {
            "symbol":"GOOG",
            "period":"1y",
            "timeframe":"1d",
            "investment":"10000",
            "pattern_type":{
                "type": "resistance",
                "window": 9,
                "similarity_difference": 0.1
            }
        }
    
    response = client.get('/patterns',json=json_input)
    assert response.status_code == 200