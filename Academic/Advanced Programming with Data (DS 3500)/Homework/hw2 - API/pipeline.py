import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




def fetch_gbif_data(species_list, year):
    """
    Takes a list and integer as parameters
    Returns a DataFrame of results from API of URL with parameters
    """
    url = "https://api.gbif.org/v1/occurrence/search"                   # string of URL, without parameters
    info = []
    min_cols = ["species", "decimalLatitude", "decimalLongitude",
                 "eventDate", "month", "stateProvince", "country",
                "coordinateUncertaintyInMeters", ]                      # Defines a list of minimum required columns to include in the DataFrame
    for a in range(len(species_list)):                                  # For a in range length of inputted list "species_list"
        for month in range(1, 13):                                      # For each iteration through the number of months
            parameters = {"decimalLatitude": "38.8,47.5",
                            "decimalLongitude": "-77.5,-66.5",
                            "year": year,
                            "scientificName": species_list[a],
                            "limit": 25,
                            "month": month}                             # Defines parameters to attach to URL
            response = requests.get(url, params=parameters)             # Sends GET request for URL with parameters
            data = response.json()                                      # Defines data as the decoded JSON response
            for b in data["results"]:                                   # For each category/parameter in the results of data
                info.append(b)                                          # Append to the list every value set in each iteration of results
    species_df = pd.DataFrame(info)                                     # Create a DataFrame from the list of results
    species_df = species_df[min_cols]                                   # Redefine "species_df" DataFrame with specified columns
    return species_df




def clean_biodiversity_data(raw_df):
    """
    Takes a DataFrame
    Returns the inputted DataFrame with null/missing values and duplicate rows removed, as well as a dictionary of cleaning metrics
    """
    original_rcount = len(raw_df)                                       # Defines the number of rows for raw_df
    date = []
    for c in range(len(raw_df)):                                        # For each row/index number of raw_df
        date.append(raw_df["eventDate"].iloc[c].split("T")[0])          # Takes each entry of the "eventDate" column and splits the date and time,
                                                                        # Joined by "T", then appends only the date to the list "date"
    raw_df["eventDate"] = pd.DataFrame(date)                            # Replaces "eventDate" column values with date instead of date and time
    clean_df = raw_df.dropna()                                          # Defines new DataFrame without rows containing null/missing values
    null_drop = original_rcount - clean_df.shape[0]                     # Defines the number of null-valued rows dropped
    clean_df = clean_df.drop_duplicates()                               # Removes duplicate rows
    dup_drop = original_rcount - clean_df.shape[0] - null_drop          # Defines the number of duplicate rows dropped
    clean_rcount = len(clean_df)                                        # Defines the number of rows for clean_df, the cleaned raw_df
    retained = round(((clean_rcount/original_rcount)*100), 2)           # Defines the percentage of rows not dropped from raw_df
    metric_dict = {"Raw Count": original_rcount, "Clean Count": clean_rcount,
                   "Null/Missing Drop": null_drop, "Duplicate Drop": dup_drop,
                   "Percent Retained": retained}                        # Defines a dictionary of cleaning metrics

    return clean_df, metric_dict




def enrich_with_state_data(cleaned_df,state_ref_df):
    """
    Takes two DataFrames
    Returns a merged DataFrame (left merge) with sorted state names and null values filled by "99999999"
    """
    merged_df = cleaned_df.merge(state_ref_df,left_on="stateProvince", right_on="state_name",
                                 how="left")                                # Left merges two dataframes on respective state columns
    # I used a left join to merge the dataFrames so that all data in cleaned_df would be included, even the stateProvince's outside of the U.S.,
    # since the state_ref_df only contains information from states within the U.S and cleaned_df includes Canadian states.
    merged_df = merged_df.sort_values("state_name").fillna(99999999)        #   Redefines and sorts the merged DataFrame, plus fills null values
    return merged_df




def calculate_analysis(enriched_df):
    """
    Takes a DataFrame
    Returns an analysis on observations per state and density along with a monthly species distribution plot
    """
    obs_count = enriched_df.groupby(by=["state_name", "area_sq_km"],
                                    as_index=False, dropna=True).size()         # Defines the count of a DataFrame grouped by "state_name" and "area_sq_km"
    density = []
    for c in range(len(obs_count)):                                             # Iterates through the number of rows in the grouped DataFrame
        dens = (obs_count["size"][c]/obs_count["area_sq_km"][c])*1000           # Divides observation count by state area*1000 to get density per 1000 km
        dens = round(float(dens),2)                                             # Redefines density as a rounded float
        density.append(dens)                                                    # Appends each observation density (per state) to the list "density"
    dens_analysis = pd.DataFrame(data={"state_name": obs_count["state_name"].to_list(),
                                    "obs_count": obs_count["size"].to_list(),
                                    "obs_per_1000km": density})                 # Defines a DataFrame of inputted DataFrame states, observation count and density
    enriched_df2 = enriched_df.copy().sort_values("month")                      # Defines a copy of "enriched_df" and sorts by month
    enriched_df2["month"] = pd.to_datetime(enriched_df["eventDate"]).dt.month_name()            # Replaces "month" values of the copy df with month names
    chart = sns.catplot(enriched_df2, kind="count", x="month", hue="species", aspect=2.0)       # Defines a plot of monthly species observation distributions
    chart.set_axis_labels("Month of Sighting", "Number of Sightings")                           # Labels the plot axes
    return dens_analysis
