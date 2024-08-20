import pytest
from app.services import fetch_stock_data
from app.models import StockData


def test_fetch_stock_data():
    data = fetch_stock_data("AAPL", period="1d", interval="1m")
    assert isinstance(data, list)
    assert all(isinstance(item, StockData) for item in data)
