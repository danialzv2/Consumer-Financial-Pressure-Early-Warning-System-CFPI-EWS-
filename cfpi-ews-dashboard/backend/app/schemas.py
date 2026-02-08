from pydantic import BaseModel
from datetime import date

class HistoricalCFPI(BaseModel):
    date: date
    state: str
    ron95: float
    ron97: float
    diesel: float
    ron95_budi95: float
    USD: float
    index: float
    Rate: float
    cfpi: float
    risk_flag: str
    fuel_pressure: float
    inflation_pressure: float
    fx_pressure: float
    policy_pressure: float




class ForecastCFPI(BaseModel):
    date: date
    state: str
    ron95: float
    ron97: float
    diesel: float
    ron95_budi95: float
    USD: float
    index: float
    Rate: float
    cfpi: float
    prob_cfpi_up_next_month: float
    direction_signal: str

