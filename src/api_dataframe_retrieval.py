import pandas as pd
import numpy as np
import requests
from json_to_df import json_to_df

def api_dataframe():

    #fuel data
    url = "https://api.data.gov.my/data-catalogue?id=fuelprice" 
    response_json = requests.get(url=url).json()
    fuel_data = json_to_df(response_json)

    #opr data
    url = "https://api.bnm.gov.my/public/opr"
    headers = {
        "Accept": "application/vnd.BNM.API.v1+json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    opr_data = json_to_df(data)

    #usd to myr data
    url = "https://api.bnm.gov.my/public/usd-interbank-intraday-rate"
    headers = {
        "Accept": "application/vnd.BNM.API.v1+json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    myr_data = json_to_df(data)

    # # Current data dataframe
    # date_data = pd.DataFrame({
    #     "date": [pd.Timestamp.today().replace(day=1)]
    # })

    #inflation data
    url = "https://api.data.gov.my/data-catalogue?id=cpi_state&divison=overall"
    response_json = requests.get(url=url).json()
    inflation_data = json_to_df(response_json)


    return fuel_data,opr_data,myr_data,inflation_data