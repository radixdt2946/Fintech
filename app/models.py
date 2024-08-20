from pydantic import BaseModel


class StockData(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    date: str
