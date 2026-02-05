from fastapi import FastAPI
from app.services import (
    get_historical_timeseries,
    get_latest_forecast_by_state,
    get_state_dashboard_view,
    get_all_states
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CFPI Early Warning System",
    version="1.0",
    debug=True
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "CFPI-EWS API running"}

@app.get("/historical/states")
def list_states():
    return get_all_states()

@app.get("/historical/state/{state_name}")
def historical_state(state_name: str):
    return get_historical_timeseries(state_name)

@app.get("/forecast/state/{state_name}")
def forecast_state(state_name: str):
    return get_latest_forecast_by_state(state_name)

@app.get("/dashboard/state/{state_name}")
def dashboard_state(state_name: str):
    return get_state_dashboard_view(state_name)

