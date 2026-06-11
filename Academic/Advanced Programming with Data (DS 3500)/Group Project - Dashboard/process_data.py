import data_acquisition as acquire
import data_cleaning as clean
import data_validation as validate
import pandas as pd
import geopandas as gpd

# this file is to create a combined pipeline that calls all the functions from the other files
# in the correct sequence, so you don't have to run one file at a time

def main():

    # ------------Data Acquisition------------

    try:
        full_data = gpd.read_parquet("data/raw_data_merged.parquet")
    except:
        # reading in the parks
        parks = acquire.get_geospatial(acquire.GEO_FILE)

        # getting the sensors - first tries for the parquet file, then runs the API calls
        try:
            sensors = pd.read_parquet("data/sensor_data.parquet")
        except:
            sensors = acquire.get_air_sensors(parks)
            sensors.to_parquet("data/sensor_data.parquet")


        # getting the air quality data
        try:
            air_data = pd.read_parquet("data/air_data.parquet")
        except:
            air_data = acquire.get_air_quality(sensors)
            air_data.to_parquet("data/air_data.parquet")

        # merging the air quality data with the park data
        park_air_data = acquire.merge_aq_data(parks, air_data)

        # getting the weather data
        try:
            weather_data = pd.read_parquet("data/weather_data.parquet")
        except:
            weather_data = acquire.get_weather(parks)
            weather_data.to_parquet("data/weather_data.parquet")



        # merging the weather data with the previous combination of air quality and park data
        full_data = acquire.merge_weather_data(park_air_data, weather_data)
        full_data.to_parquet("data/raw_data_merged.parquet")

    #print(full_data)

    # ------------Data Cleaning+Validation------------

    clean_df = clean.clean_data(full_data)
    clean.save_data(clean_df, "data/cleaned_data.parquet")

if __name__=="__main__":
    main()