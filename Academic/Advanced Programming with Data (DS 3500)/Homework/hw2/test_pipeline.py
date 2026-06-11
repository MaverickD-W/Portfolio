
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pipeline
import pytest


def data_acquisition():
    """
    Tests the loading and creation of the DataFrame from API data
    """
    species_list = ["Sturnus_vulgaris", "Ardea_herodias", "Cardinalis_cardinalis"]
    data = pipeline.fetch_gbif_data(species_list, 2023)

    assert len(data) > 100*len(species_list),                   "Not enough observations"
    assert "species" in data.columns,                           "Need species column"
    assert "decimalLongitude" in data.columns,                  "Need decimalLongitude column"
    assert "decimalLatitude" in data.columns,                   "Need decimalLatitude column"
    assert "eventDate" in data.columns,                         "Need eventDate column"
    assert "stateProvince" in data.columns,                     "Need stateProvince column"
    assert "coordinateUncertaintyInMeters" in data.columns,     "Need coordinateUncertaintyInMeters column"


def cleaning_and_metrics():
    """
    Tests the cleaning of the API DataFrame
    """
    species_list = ["Sturnus_vulgaris", "Ardea_herodias", "Cardinalis_cardinalis"]
    data = pipeline.fetch_gbif_data(species_list, 2023)

    clean_data,cleaning_metrics = pipeline.clean_biodiversity_data(data)

    assert clean_data.isna().sum().all() == 0,            "Should be no null values"
    assert clean_data.duplicated().sum() == 0,      "Should be no duplicate rows"
    assert len(clean_data) <= len(data),         "0 or more rows should be removed in cleaning"
    assert len(data) >= 100*len(species_list),      "Should be at least 100 observations per species after cleaning"


def data_enrichment():
    """
    Tests the merging of the API DataFrame and state_reference DataFrame
    """
    species_list = ["Sturnus_vulgaris", "Ardea_herodias", "Cardinalis_cardinalis"]
    data = pipeline.fetch_gbif_data(species_list, 2023)
    clean_data, cleaning_metrics = pipeline.clean_biodiversity_data(data)

    state_info = pd.read_csv("state_reference.csv")
    combined_df = pipeline.enrich_with_state_data(clean_data, state_info)

    assert "state_name" in combined_df.columns,         "Need state_name"
    assert "abbreviation" in combined_df.columns,       "Need state_abbreviation"
    assert "region" in combined_df.columns,             "Need region"
    assert "area_sq_km" in combined_df.columns,         "Need area_sq_km"


def main():
    data_acquisition()
    cleaning_and_metrics()
    data_enrichment()

if __name__ == "__main__":
    main()