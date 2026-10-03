import pandas as pd
from pydantic import BaseModel,computed_field


def load_data():
    """
    Loads the Subway maintenance parquet files for February 2026
    Returns a dataframe with data from each day in February 2026
    """
    url_p1 = "https://performancedata.mbta.com/lamp/subway-on-time-performance-v1/"
    url_p3 = "-subway-on-time-performance-v1.parquet"
    sub_df = pd.DataFrame()                             # Creates a blank dataframe

    for day in range(1,29):                             # Iterates through the days of February
        if day < 10:                                    # For single digit days
            date = "0" + str(day)                       # Adds a zero in front and makes the day a string
        else:                                           # Converts double-digit days to strings
            date = str(day)
        url_p2 = "2026-02-"+date                        # Completes the date in the url
        url = url_p1 + url_p2 + url_p3                  # Combines all components of the url
        data = pd.read_parquet(url)                     # Reads and stores each day's parquet
        data = data[data["trunk_route_id"] == "Green"]      # Selects the Green Line for trunk_route_id
        sub_df = pd.concat([sub_df, data],
                           ignore_index=True)           # Adds each day to the "sub_df" dataframe and reindexes
    return sub_df                                   # Returns a dataframe with each 02/2026 day from the Green Line


# These were temporary commands for caching the parquet data
# sub_df.to_parquet("feb_data.parquet")
# sub_df = pd.read_parquet("feb_data.parquet")


def clean_data(df):
    """
    Takes a dataframe
    Cleans the dataframe and returns a list of end-to-end travel times based on "service_date", "trip_id"
    """
    required_cols = ["trip_id", "stop_id", "stop_timestamp","service_date",
                     "travel_time_seconds", "scheduled_travel_time",
                     "parent_station", "trunk_route_id"]                    # Defines a list of required columns
    df.sort_values(["service_date","stop_timestamp"], inplace=True)
    df.drop_duplicates(subset=["stop_id", "trip_id"], inplace=True)
    df.dropna(subset=required_cols, inplace=True, ignore_index=True)
    end_to_end = df.groupby(by=["service_date","trip_id"], as_index=False).agg(
        {"travel_time_seconds": "sum"})             # Groups by "service_date" and "trip_id", then sums based on "travel_time_seconds"
    end_to_end.rename(columns={"travel_time_seconds": "end_to_end_time"},
                      inplace=True)                 # Renames summation column of "end_to_end" dataframe
    new_df = df.merge(end_to_end)
    return new_df


def sort_geo(df):
    """
    Takes a dataframe
    Returns the dataframe sorted by "direction", "trip_id", "stop_count" to get geogrpahic order
    """
    df.sort_values(["direction", "trip_id", "stop_count"], ascending=False, inplace=True, ignore_index=True)


def destination(df):
    """
    Takes a dataframe (ideally after using function "sort_geo")
    Returns list of end destinations/stations for train line
    """
    lst = df["parent_station"].unique().tolist()
    dest = [place.split("place-")[1] for place in lst]
    return dest


def main():
    sub_df = load_data()
    sub_df = clean_data(sub_df)
    sort_geo(sub_df)
    stations = destination(sub_df)
    return sub_df, stations

if __name__ == "__main__":
    main()

