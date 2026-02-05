import pandas as pd
from data_preprocessing import preprocessing
from data_ml_evaluation import ml_evaluation
from data_merging import merging
def main():

    data = preprocessing()
    data.to_csv("../Consumer-Financial-Pressure-Early-Warning-System-CFPI-EWS-/cfpi-ews-dashboard/backend/data/data.csv", index=False)

    ml_data = ml_evaluation(data)
    ml_data.to_csv("../Consumer-Financial-Pressure-Early-Warning-System-CFPI-EWS-/cfpi-ews-dashboard/backend/data/cfpi_direction_forecast.csv", index=False)
    
if __name__ == "__main__":
    main()
