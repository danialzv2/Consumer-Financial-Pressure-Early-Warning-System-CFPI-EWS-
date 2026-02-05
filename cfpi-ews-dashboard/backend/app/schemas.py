from pydantic import BaseModel
from datetime import date

class HistoricalCFPI(BaseModel):
    date: date
    state: str
    cfpi: float
    risk_flag: str
    fuel_pressure: float
    inflation_pressure: float
    fx_pressure: float
    policy_pressure: float


class ForecastCFPI(BaseModel):
    date: date
    state: str
    cfpi: float
    prob_cfpi_up_next_month: float
    direction_signal: str
