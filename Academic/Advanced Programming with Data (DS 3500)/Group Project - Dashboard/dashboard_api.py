import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt



##-- DATA LAYER --##


data_path = "data/cleaned_data.parquet"
park_col = "UNIT_NAME"
date_col = "date"
mean_t = "mean_temp"
max_t = "max_temp"
min_t = "min_temp"
wind_s = "wind_speed"
wind_g = "wind_gusts"
precip_col = "precipitation"
factor_cols = [mean_t, max_t, min_t, wind_s, wind_g, precip_col]
aq_names = ["so2", "pm25", "pm10", "co", "o3", "no2"]


class ParkDash:
    def __init__(self, path):
        self.park_df = gpd.read_parquet(path)         # functions same as pd.read_parquet() but has geometry

    def get_parks(self):
        """returns a list of the parks in the dataset"""
        return self.park_df[park_col].unique().tolist()

    def get_subset(self, parks="All", params=factor_cols+aq_names):
        """gets a subset of certain specific parks"""
        copy = self.park_df.copy()
        # if "All" is selected, it doesn't bother selecting a specific one
        if parks != "All":
            copy = copy[copy[park_col] == parks]

        cols = ["UNIT_NAME", "date_month", "date"]
        for i in params:
            cols.append(i)
        copy = copy[cols]
        return copy

    def get_avg(self, params=factor_cols+aq_names, parks="All"):

        park_subset = self.get_subset(parks)

        monthly_data = park_subset.groupby(["UNIT_NAME", "date_month"], as_index=False).agg({i: "mean" for i in params})
        return  monthly_data
