import geopandas as gpd
from pydantic import ValidationError
from data_validation import ParkConditions


def clean_data(df):
    """"
    Takes a DataFrame
    Drops null values and duplicate rows
    Returns a cleaned DataFrame with only the desired columns
    """
    df2 = df.copy()                                                     # Creates a copy of the original DataFrame
    req_cols = ["UNIT_NAME", "date", "sensor_latitude", "sensor_longitude",
                "latitude", "longitude", "geometry",
                "so2", "pm25", "pm10", "co", "o3", "no2",
                "mean_temp", "max_temp", "min_temp",
                "wind_speed", "wind_gusts", "precipitation"]            # Defines the desired columns
    not_null = ["UNIT_NAME", "UNIT_TYPE", "date", "sensor_latitude",
                "sensor_longitude", "mean_temp", "max_temp", "min_temp",
                "latitude", "longitude", "geometry",
                "wind_speed", "wind_gusts", "precipitation"]            # Defines the columns that should not be null
    df2.drop_duplicates(inplace=True)        # Drop duplicate rows
    df2.dropna(subset=not_null, inplace=True, ignore_index=True)        # Drop rows with null values
    return df2[req_cols]                                # Return the cleaned DataFrame with only the desired columns

def validate_data(df):
    """
    Takes a DataFrame
    Uses class from "data_validation.py" to validate data from "date" column
    """
    vals = []
    errors = 0
    for _, row in df.iterrows():
        try:
            rows = ParkConditions(**row)
            vals.append(rows)
        except ValidationError:
            errors += 1
            continue
        if errors:
            print(f"{errors} 'date' validation errors encountered")

def add_months(df):
    """
    Takes a DataFrame
    Extracts the months from the "date" column and inserts a column of the months into the DataFrame
    """
    dates = df["date"].tolist()
    months = [a.split("-")[1] for a in dates]
    df.insert(2, "date_month", months)

def save_data(df, new_path):
    """
    Takes a DataFrame and desired filepath
    Saves a parquet of the inputted DataFrame, using the inputted filepath
    """
    df.to_parquet(new_path)


def main():
    """
    Loads and defines the data as a DataFrame
    Cleans a copy of the DataFrame
    Saves the cleaned DataFrame
    """
    raw_df = gpd.read_parquet("data/raw_data_merged.parquet")
    clean_df = clean_data(raw_df)
    validate_data(clean_df)
    add_months(clean_df)
    save_data(clean_df, "data/cleaned_data.parquet")

if __name__ =="__main__":
    main()