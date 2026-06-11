import pandas as pd
import geopandas as gpd
import requests
import json
from time import sleep
import matplotlib.pyplot as plt

# for accessing the .env file so we can store API keys in there
import os
import dotenv
dotenv.load_dotenv()

GEO_FILE = "data/nps_boundary.zip"

OPENAQ_LOCATION_URL = "https://api.openaq.org/v3/locations"
BASE_OPENAQ_DATA_URL = "https://api.openaq.org/v3/sensors/<id>/measurements/daily"
OPENAQ_KEY = os.environ.get("OPENAQ_KEY")
AQ_RADIUS = 10000
AQ_START_DATE = "2025-01-01T00:00:00Z"
AQ_END_DATE = "2025-12-31T00:00:00Z"

# fields to keep from the API return
KEPT_FIELDS = []

WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"
# measured values to get for each day
DAILY_WEATHER_PARAMS = ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
                       "wind_speed_10m_max","wind_gusts_10m_max",
                       "precipitation_sum"]
# TODO: figure out what an optimal date range is
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

def get_geospatial(filename):
    """return a geodataframe formed from a shapefile"""
    gdf = gpd.read_file(filename)

    # adding latitude and longitude values if the dataset doesn't already include them
    if "latitude" not in gdf.columns:
        gdf['latitude'] = gdf.centroid.y
    if "longitude" not in gdf.columns:
        gdf['longitude'] = gdf.centroid.x

    # creating an int version of the coordinates to hopefully merge without floating point errors
    gdf["merge_longitude"] = (round(gdf["longitude"]*100,0)).astype(int)
    gdf["merge_latitude"] = (round(gdf["latitude"]*100,0)).astype(int)
    return gdf

def _retry_api(url, params=None, headers=None, max_retries=8):
    """
    Queries an API multiple times with exponential backoff

    :param url: string - API endpoint
    :param params: dict - query parameters
    :param headers: dict - request headers
    :param max_retries: int - max number of retry attempts

    Returns:
        dict: JSON response, or raises an exception if all retries fail
    """

    # starting wait time
    wait_time = 1

    # setting this to some default value so pycharm stops bothering me about it
    response = requests.get(url, params=params, headers=headers)
    for attempt in range(max_retries):
        if attempt != 0:
            response = requests.get(url, params=params, headers=headers)
        # exponential wait time if get request fails
        if response.status_code == 429:
            sleep(wait_time)
            #print(f"completed {wait_time} sleep cycle")
            wait_time *= 2
        elif response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception("401 - Unauthorized. Check your API key")
        elif response.status_code == 403:
            raise Exception("403 - Access forbidden")
        elif response.status_code == 404:
            raise Exception("404 - Page not found. Check URL")
        else:
            raise Exception("Unspecified issue")

    raise Exception("Number of 429 errors exceeded retry limit")

def _get_closest_sensor(park, results):
    """
    gets the closest sensor to a park from those within a 10km radius

    :param park: a single row of a geodataframe about a specific park
    :param results: a list of dictionaries from the 'results' section of an API return
    :return: the id, coordinates, and associated park coordinates of the sensor that's closest
            to that park's center
    """
    sensor = pd.DataFrame()
    for i in range(len(results)):
        # setting up a df to store the data for each sensor near that park's coordinates
        sensor.loc[i, "id"] = results[i]["id"]
        sensor.loc[i, "sensor_latitude"] = results[i]["coordinates"]["latitude"]
        sensor.loc[i, "sensor_longitude"] = results[i]["coordinates"]["longitude"]
        sensor.loc[i, "distance"] = results[i]["distance"]

        sensor.loc[i, "merge_latitude"] = park['merge_latitude']
        sensor.loc[i, "merge_longitude"] = park['merge_longitude']

    # getting just the closest station
    sensor = sensor.sort_values(by=["distance"])
    sensor = sensor.iloc[[0], :]

    return sensor

def get_air_sensors(gdf):
    """
    get the id and coordinates of the sensors within 10km from the park's center,
    and returns specifically the closest one

    (radius could potentially do with some adjusting for optimal results)

    :param gdf: geodataframe with locations to get data around
    :return: dataframe of sensor ids to get measurements from, plus some details
            about their position and associated park
    """

    headers = {"X-API-Key": OPENAQ_KEY}
    # finding air quality within a radius around the center of each park
    params = {"radius": AQ_RADIUS}

    sensor_data = pd.DataFrame()

    k=1
    for _, park in gdf.iterrows():
        print("sensor", k) # counting so i can tell the process is progressing
        k+=1
        params["coordinates"] = f"{park['latitude']},{park['longitude']}"
        row = _retry_api(OPENAQ_LOCATION_URL, params=params, headers=headers)

        results = row["results"] # getting the results from each place called
        if len(results) != 0: # checking if the results isn't empty

            sensor = _get_closest_sensor(park, results)

            sensor_data = pd.concat([sensor_data, sensor], ignore_index=True)

    return sensor_data


def get_air_quality(sensors):
    """
    gets air quality data from sensors within a 15 km radius around each park's center

    :param sensors: dataframe of the sensor IDs and a few other pieces of info
    :return: a dataframe of the different sensor readings and the coordinates of the sensor
            they came from
    """
    headers={"X-API-Key":OPENAQ_KEY}
    parameters = {"datetime_from":AQ_START_DATE, "datetime_to":AQ_END_DATE, "limit":1000}

    # setting up an empty dataframe to concat into
    air_data = pd.DataFrame()

    k=1
    # going through all the sensors and querying the API for each of them
    for _, sensor in sensors.iterrows():
        print("air quality", k)
        k+=1
        url = BASE_OPENAQ_DATA_URL.replace("<id>",str(int(sensor["id"])))

        data = _retry_api(url, headers=headers, params=parameters)
        # TODO: add pagination if we want data from more than one year

        # converting the results of the API call into a dataframe
        df = _convert_air_to_dataframe(data, sensor)

        # concatenating the df of the sensor data to the overall dataframe
        air_data = pd.concat([air_data, df], ignore_index=True)

    return air_data


def _convert_air_to_dataframe(data, sensor):
    """
    converts the list produced by the API into a dataframe of just the measured values
    (plus the date they came from and their location)

    :param data: a list of dicts as given by an API's returned JSON files
    :param sensor: a row of the sensor dataframe
    :return: a dataframe of the values and the date they're from
    """
    df = pd.DataFrame()

    for i, result in enumerate(data["results"]):
        if len(result) != 0:
            df.loc[i, result["parameter"]["name"]] = result["value"]
            df.loc[i, "date"] = result["period"]["datetimeFrom"]["utc"].split("T")[0]

            # adding the latitude and longitude to each of the rows in that sensor-specific
            # meassurement df
            df.loc[i, "sensor_latitude"] = sensor["sensor_latitude"]
            df.loc[i, "sensor_longitude"] = sensor["sensor_longitude"]
            df.loc[i, "merge_latitude"] = int(sensor["merge_latitude"])
            df.loc[i, "merge_longitude"] = int(sensor["merge_longitude"])

    return df


def get_weather(gdf):
    """
    gets daily weather data for each park over the given span of dates

    :param gdf: geodataframe with locations to get the weather around

    :return: a dataframe of the results
    """
    #data = []
    data_df = pd.DataFrame()
    params = {"start_date":START_DATE, "end_date":END_DATE,
              "daily":DAILY_WEATHER_PARAMS # what attributes to get each day
              }

    k=1
    # going through all the parks and calling the API for each one's center latitude/longitude
    for _,park in gdf.iterrows():
        print("weather", k)
        k+=1
        params["latitude"] = park["latitude"]
        params["longitude"] = park["longitude"]

        weather_data = _retry_api(WEATHER_URL, params=params)
        #data.append(weather_data)

        weather_df = _single_park_weather_to_df(weather_data)

        # I keep having no rows show up when merging on these columns, so maybe doing this will help
        weather_df["merge_latitude"] = int(park["merge_latitude"])
        weather_df["merge_longitude"] = int(park["merge_longitude"])

        data_df = pd.concat([data_df, weather_df], ignore_index=True)

        # saving an incomplete versions so I can at least have that if it fails
        data_df.to_parquet("data/weather_data.parquet")

    #return _weather_to_df(data)
    return data_df


# old version from when i converted the whole set of weather data to a df at the end
# def _weather_to_df(data):
#     """
#     converts all parks' weather data from list of dicts format (from the API) to a
#     dataframe format
#
#     :param data: a list of dicts like is returned from a series of API calls
#     :return: a dataframe
#     """
#     weather_df = pd.DataFrame()
#
#     for i in range(len(data)):
#         for j in range(len(data[i]["daily"]["time"])):
#             df = pd.DataFrame()
#             df.loc[j, "date"] = data[i]["daily"]["time"][j]
#             df.loc[j, "latitude"] = data[i]["latitude"]
#             df.loc[j, "longitude"] = data[i]["longitude"]
#
#             df.loc[j, "mean temp"] = data[i]["daily"]["temperature_2m_mean"][j]
#             df.loc[j, "max temp"] = data[i]["daily"]["temperature_2m_max"][j]
#             df.loc[j, "mean min"] = data[i]["daily"]["temperature_2m_min"][j]
#             df.loc[j, "wind speed"] = data[i]["daily"]["wind_speed_10m_max"][j]
#             df.loc[j, "wind gusts"] = data[i]["daily"]["wind_gusts_10m_max"][j]
#             df.loc[j, "precipitation"] = data[i]["daily"]["precipitation_sum"][j]
#
#             weather_df = pd.concat([weather_df, df], ignore_index=True)
#
#     return weather_df

def _single_park_weather_to_df(data):
    """
    converts one park's weather data to a dataframe and returns it
    :param data: dictionary from open-meteo historical weather API
    :return: dataframe of the date, latitude, longitude, and relevant measures
    """
    df = pd.DataFrame()
    for j in range(len(data["daily"]["time"])):
        df.loc[j, "date"] = str(data["daily"]["time"][j])
        df.loc[j, "merge_latitude"] = int(round(data["latitude"]*100,0))
        df.loc[j, "merge_longitude"] = int(round(data["longitude"]*100,0))

        df.loc[j, "mean_temp"] = data["daily"]["temperature_2m_mean"][j]
        df.loc[j, "max_temp"] = data["daily"]["temperature_2m_max"][j]
        df.loc[j, "min_temp"] = data["daily"]["temperature_2m_min"][j]
        df.loc[j, "wind_speed"] = data["daily"]["wind_speed_10m_max"][j]
        df.loc[j, "wind_gusts"] = data["daily"]["wind_gusts_10m_max"][j]
        df.loc[j, "precipitation"] = data["daily"]["precipitation_sum"][j]

    return df

def merge_aq_data(park_df, air_df):
    """
    merges the park data with the attribute data from air_df and weather_df
    :param park_df: geodataframe of the park regions
    :param air_df: dataframe of the air quality stuff
    :return: the merged dataframe containing all the locations with data
    """

    # this if/else statement is so that if an empty dataframe gets passed, it returns
    # an empty dataframe instead of gettin a merge error
    if len(park_df) !=0 and len(air_df) !=0:
        df = pd.merge(left=park_df, right=air_df, left_on=["merge_latitude", "merge_longitude"],
                  right_on=["merge_latitude", "merge_longitude"])
        return df
    else:
        return pd.DataFrame()



def merge_weather_data(park_df, weather_df):
    """
    merges the park data with the attribute data from air_df and weather_df
    :param park_df: geodataframe of the park regions merged with the air quality data
    :param weather_df: dataframe of the weather stuff
    :return: the merged dataframe
    """

    weather_df["merge_latitude"] = weather_df["merge_latitude"].astype(int)
    weather_df["merge_longitude"] = weather_df["merge_longitude"].astype(int)

    if len(park_df) != 0 and len(weather_df) != 0:
        df = pd.merge(left=park_df, right=weather_df, left_on=["merge_latitude", "merge_longitude", "date"],
                  right_on=["merge_latitude", "merge_longitude", "date"] )
        return df
    else:
        return pd.DataFrame()

def main():
    parks = get_geospatial(GEO_FILE)
    pd.set_option('display.max_columns', None)
    #print(parks)
    #print(len(parks))

    # getting the sensors
    sensors = get_air_sensors(parks)
    sensors.to_parquet("data/sensor_data.parquet")
    #sensors = pd.read_parquet("data/sensor_data.parquet")
    #print(len(sensors))
    #print(sensors)

    # getting the air quality data
    air_data = get_air_quality(sensors)
    air_data.to_parquet("data/air_data.parquet")
    #air_data = pd.read_parquet("data/air_data.parquet")
    #print(air_data)

    # merging the air quality data with the park data
    park_air_data = merge_aq_data(parks, air_data)
    #print(park_air_data)

    # getting the weather data for just the places that remain in that merged dataframe
    weather_data = get_weather(parks)
    weather_data.to_parquet("data/weather_data.parquet")
    #weather_data = pd.read_parquet("data/weather_data.parquet")
    #print(weather_data)

    full_data = merge_weather_data(park_air_data, weather_data)

    #print(full_data)

    full_data.to_parquet("data/raw_data_merged.parquet")


if __name__ == "__main__":
    main()