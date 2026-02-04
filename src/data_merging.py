import pandas as pd
from api_dataframe_retrieval import api_dataframe

def merging():

    #####Merging
    fuel_data, opr_data, myr_data, inflation_data = api_dataframe()

    #fuel data
    fuel_data["date"] = pd.to_datetime(fuel_data["date"])
    fuel_data["date"] = pd.to_datetime(fuel_data["date"])
    one_year_ago = fuel_data["date"].max() - pd.DateOffset(years=1)
    fuel_data = fuel_data[fuel_data["date"] >= one_year_ago]

    #myr to usd data
    myr_data["date"] = pd.to_datetime(myr_data["data.date"], dayfirst=True)
    myr_data = myr_data.drop(columns=["data.date"])

    #opr data
    opr_data["date"] = pd.to_datetime(opr_data["data.date"], dayfirst=True)
    opr_data = opr_data.drop(columns=["data.date"])

    #inflation data
    inflation_data["date"] = pd.to_datetime(inflation_data["date"])

    inflation_data = inflation_data[ inflation_data["division"] == "overall" ]
    fuel_data = fuel_data[ fuel_data["series_type"] == "level" ]
    

    #Merging data
    merged = fuel_data.merge(myr_data, on="date", how="outer") \
                  .merge(inflation_data, on="date", how="outer") \
                  .merge(opr_data, on="date", how="outer") \

    cols_to_fill = ["ron95", "ron97", "diesel", "ron95_budi95"]
    merged[cols_to_fill] = merged[cols_to_fill].ffill()

    cols = ['data.highest_rate', 'data.lowest_rate', 'data.new_opr_level']
    for col in cols:
        non_null_values = merged[col].dropna().unique()

        if len(non_null_values) == 1:
            merged[col] = merged[col].fillna(non_null_values[0])

    oldest_date = fuel_data["date"].min()
    merged = merged[merged["date"] >= oldest_date]
    merged = merged.drop(
        columns=[
            "ron95_skps",
            "series_type",
            "diesel_eastmsia",
            "data.lowest_rate",
            "data.year",
            "data.change_in_opr",
            "meta.last_updated_x",
            "meta.total_result_x",
            "meta.last_updated_y",
            "meta.total_result_y"
        ],
        errors="ignore"   # prevents crash if column missing
    )    
    merged["ron95_budi95"] = merged["ron95_budi95"].fillna(merged["ron95"])
    merged = merged.dropna(subset=["state"])

    merged = merged.rename(
        columns={
            "data.highest_rate": "USD",
            "data.new_opr_level": "Rate"
        }
    )

    #################### Append & Overwrite Function ################################
    latest_date = merged["date"].max()
    merged = merged.loc[merged["date"] == latest_date]

    cleaned_data = pd.read_csv("../Consumer-Financial-Pressure-Early-Warning-System-CFPI-EWS-/data/cleaned_data.csv")
    cleaned_data["date"] = pd.to_datetime(cleaned_data["date"])
    cleaned_data = cleaned_data.drop(columns=["Unnamed: 0"])
    latest_date_cleaned = cleaned_data["date"].max()

    row_to_add = merged.loc[merged["date"] == latest_date].copy()
    row_to_add["date"] = row_to_add["date"] + pd.DateOffset(months=1)
    shifted_date = row_to_add["date"].iloc[0]

    if shifted_date == latest_date_cleaned:
        cleaned_data = cleaned_data.loc[
            cleaned_data["date"] != shifted_date
        ]

        cleaned_data = pd.concat(
            [cleaned_data, row_to_add],
            ignore_index=True
        )

    else:
        cleaned_data = pd.concat(
            [cleaned_data, row_to_add],
            ignore_index=True
        )

    cleaned_data = (
        cleaned_data
        .sort_values("date")
        .reset_index(drop=True)
    )
    ################################################################################

    return cleaned_data


