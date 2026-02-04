import pandas as pd

def json_to_df(data):
    if isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            return pd.json_normalize(data)
        else:
            return pd.DataFrame({"value": data})

    elif isinstance(data, dict):
        return pd.json_normalize(data)

    else:
        return pd.DataFrame({"value": [data]})