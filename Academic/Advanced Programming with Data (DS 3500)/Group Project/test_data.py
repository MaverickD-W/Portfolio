import pytest
from unittest.mock import patch
import pandas as pd
import geopandas as gpd

import data_acquisition as acquisition
import data_cleaning as clean

# tests must cover
#   •Data loading/fetching functions
#   •Data cleaning functions (e.g., "test that duplicates are removed")
#   •Merge logic (e.g., "test that merge preserves expected rows")
#   •Data validation (e.g., "test that values are in valid ranges")

@pytest.fixture
def fake_parks():
    """creating a dataframe of three fake parks, which only have merge coordinates since that's all we
    really care about"""
    df = pd.DataFrame({"merge_latitude":[10, 20, 30], "merge_longitude":[40, 50, 60]})
    return df

@pytest.fixture
def fake_sensor_results():
    """creating a list of dicts with id, coordinate, and distance results to represent a sensor"""
    return [
        {"id":1, "coordinates":{"latitude":11, "longitude":12}, "distance":20},
        {"id":2, "coordinates":{"latitude":10, "longitude":11}, "distance":10},
        {"id":3, "coordinates":{"latitude":12, "longitude":13}, "distance":30}
    ]

def test_closest_sensor(fake_parks, fake_sensor_results):
    """testing if the system properly selects the closest sensor to the park's center"""
    park = fake_parks.loc[0, :]
    closest = acquisition._get_closest_sensor(park, fake_sensor_results)
    closest = closest.reset_index(drop=True)

    assert closest.iloc[0].all() == pd.DataFrame({"id":[2], "sensor_latitude":[10],
                                    "sensor_longitude":[11], "distance":[10], "merge_latitude":[10],
                                    "merge_longitude":[40]}).iloc[0].all()

@pytest.fixture
def fake_aq_results_raw():
    """creating a dict of things as a fake API result"""

    response = {
        "results":[{"parameter":{"name":"pm25"},
                    "value":25,
                    "period":{"datetimeFrom":{"utc":"2025-01-02T00:00:00"}}
                    },
                   {"parameter": {"name": "co"},
                    "value": 23,
                    "period": {"datetimeFrom": {"utc":"2025-01-03T00:00:00"}}
                    }]}

    return response

@pytest.fixture
def fake_sensor_row():
    """returns a fake row of a dataframe containing sensor information"""
    sensor = pd.DataFrame({
        "sensor_latitude":[1.2],
        "sensor_longitude":[2.3],
        "merge_latitude":[34],
        "merge_longitude":[45]
    })

    return sensor.loc[0]

def test_air_to_df(fake_aq_results_raw, fake_sensor_row):
    df = acquisition._convert_air_to_dataframe(fake_aq_results_raw, fake_sensor_row)

    assert df.equals(pd.DataFrame({
        "pm25":[25.0, None],
        "date":["2025-01-02", "2025-01-03"],
        "sensor_latitude": [1.2, 1.2],
        "sensor_longitude": [2.3, 2.3],
        "merge_latitude": [34.0, 34.0],
        "merge_longitude": [45.0, 45.0],
        "co": [None, 23.0]
    }))
    # for some reason it requires the .0 to run successfully, which is weird to me but I don't
    # think should meaningfully affect our results aside from on merging, which I've already
    # fought to make work


@pytest.fixture
def fake_aq_df():
    """creating a dataframe of fake air quality results"""
    df = pd.DataFrame({
        "merge_latitude":[10, 10, 20],
        "merge_longitude":[40, 40, 50],
        "sensor_latitude":[10, 10, 11],
        "sensor_longitude":[11, 11, 12],
        "pm25":[22, 24, None],
        "date":["2025-01-01", "2025-02-02", "2025-03-03"]
    })

    return df

@pytest.fixture
def fake_weather_results():
    """creating a dataframe of fake weather results"""

    df = pd.DataFrame([
        {"merge_latitude":10, "merge_longitude":40, "date":"2025-01-01", "temp":2}, #all match
        {"merge_latitude":10, "merge_longitude":40, "date":"2025-01-01", "temp":42}, #all match, another value
        {"merge_latitude": 40, "merge_longitude": 40, "date": "2025-01-01", "temp": 23}, # nonexistant latitude
        {"merge_latitude": 10, "merge_longitude": 40, "date": "2025-01-02", "temp": 22}, #nonexistant date
        {"merge_latitude": 20, "merge_longitude": 50, "date": "2025-03-03", "temp": 19} # all match a different row
    ])
    return df

def test_first_merge(fake_parks, fake_aq_df):
    """testing if the first merge between parks and air quality works how i expect
    """
    park_aq_df = acquisition.merge_aq_data(fake_parks, fake_aq_df)

    assert park_aq_df.equals(pd.DataFrame({
        "merge_latitude":[10, 10, 20],
        "merge_longitude":[40, 40, 50],
        "sensor_latitude": [10, 10, 11],
        "sensor_longitude": [11, 11, 12],
        "pm25":[22, 24, None],
        "date":["2025-01-01", "2025-02-02", "2025-03-03"]
    }))

def test_second_merge(fake_parks, fake_aq_df, fake_weather_results):
    """testing if the second merge (parks and air quality + weather) works how i expect"""
    park_aq_df = acquisition.merge_aq_data(fake_parks, fake_aq_df)

    full_df = acquisition.merge_weather_data(park_aq_df, fake_weather_results)

    assert full_df.equals(pd.DataFrame([
        {"merge_latitude":10, "merge_longitude":40, "sensor_latitude":10,
         "sensor_longitude":11, "pm25":22,  "date":"2025-01-01", "temp":2},
        {"merge_latitude":10, "merge_longitude":40, "sensor_latitude":10,
         "sensor_longitude": 11, "pm25": 22, "date": "2025-01-01", "temp": 42},
        {"merge_latitude":20, "merge_longitude":50, "sensor_latitude":11,
         "sensor_longitude": 12, "pm25": None, "date": "2025-03-03", "temp": 19}
    ]))

@pytest.fixture
def fake_merged_raw_df():
    """creating a fake versjion of the the raw merged dataframe """

    req_cols = ["UNIT_NAME", "date", "sensor_latitude", "sensor_longitude",
                "latitude", "longitude", "geometry",
                "so2", "pm25", "pm10", "co", "o3", "no2",
                "mean_temp", "max_temp", "min_temp",
                "wind_speed", "wind_gusts", "precipitation"]
    not_null = ["UNIT_NAME", "UNIT_TYPE", "date", "sensor_latitude",
                "sensor_longitude", "mean_temp", "max_temp", "min_temp",
                "wind_speed", "wind_gusts", "precipitation"]

    # making a dict of values in the necessary columns
    df_dict = {val:[1,1,2,3,5,6,7,8] for val in (req_cols + ["UNIT_TYPE"])}

    # adding some null values to drop/not drop
    df_dict["UNIT_TYPE"][4] = None
    df_dict["wind_gusts"][5] = None
    df_dict["pm25"][6] = None

    df = pd.DataFrame(df_dict)

    return df

def test_cleaning(fake_merged_raw_df):
    # creating the dictionary of expected results
    req_cols = ["UNIT_NAME", "date", "sensor_latitude", "sensor_longitude",
                "latitude", "longitude", "geometry",
                "so2", "pm25", "pm10", "co", "o3", "no2",
                "mean_temp", "max_temp", "min_temp",
                "wind_speed", "wind_gusts", "precipitation"]
    df_dict = {val:[1,2,3,7,8] for val in (req_cols)}

    #converting these to floats because the output has them that way for some reason
    df_dict["pm25"] = [1.0, 2.0, 3.0, None, 8.0]
    df_dict["wind_gusts"] = [1.0, 2.0, 3.0, 7.0, 8.0]

    df = pd.DataFrame(df_dict)

    assert clean.clean_data(fake_merged_raw_df).equals(df)


def test_load_data():
    """
    Tests the loading of the raw merged data
    """
    raw_df = pd.read_parquet("data/raw_data_merged.parquet")
    assert len(raw_df["UNIT_NAME"].unique())*300 <= len(raw_df),    "Should be at least 300 observations per park"

    req_cols = ["UNIT_NAME", "date", "sensor_latitude", "sensor_longitude",
                "latitude", "longitude", "geometry",
                "so2", "pm25", "pm10", "co", "o3", "no2",
                "mean_temp", "max_temp", "min_temp",
                "wind_speed", "wind_gusts", "precipitation"]        # Defines the desired columns
    for col in req_cols:                                            # Check that all desired columns are present
        assert col in raw_df.columns,       f"Missing {col} column"

def test_cleaning_data():
    """
    Tests the cleaning of the raw API DataFrame
    """
    raw_df = pd.read_parquet("data/raw_data_merged.parquet")
    clean_df = clean.clean_data(raw_df)

    assert clean_df.duplicated().sum() == 0,      "Should be no duplicate rows"
    assert len(clean_df) <= len(raw_df),         "0 or more rows should be removed in cleaning"
    assert len(clean_df) >= len(raw_df["UNIT_NAME"].unique())*300,      "Not enough observations"

def test_saving_data():
    """
    Ensures the cleaned DataFrame is properly saved as a parquet file
    """
    raw_df = pd.read_parquet("data/raw_data_merged.parquet")
    clean_df = clean.clean_data(raw_df)
    clean.save_data(clean_df, "data/cleaned_data.parquet")
    saved_df = pd.read_parquet("data/cleaned_data.parquet")

    assert len(saved_df) == len(clean_df),      "Incorrect number of observations in saved file"