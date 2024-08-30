import pytest

def test_quote(client):
    
    response = client.get('/quote?symbol=AAPL')
    assert response.status_code == 200
    assert 'price' in response.json