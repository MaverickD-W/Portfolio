import pandas as pd
import geopandas as gpd
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.animation import FuncAnimation
from plotly.subplots import make_subplots

from dashboard_api import ParkDash



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

data = ParkDash(data_path)

def format_text(text):
    """replaces underscores with spaces and converts to title case"""
    return (" ").join((text).split("_")).title()

def create_choropleth(gdf, value):
    """
    create a choropleth (map using color to encode the value of an attribute in different areas)
    from a geodataframe

    :param gdf: a geodataframe with the geometry data of the places we're making a map of
    :param value: str - the name of the column of the attribute we're plotting
    :return: a plot of the map
    """

    gdf2 = gdf.copy()

    background_map = gpd.read_file("data/US_State_Boundaries.zip")

    # setting them on the same crs rendering so they line up(?)
    background_map = background_map.to_crs(gdf2.crs)

    # getting the mean yearly value for each park
    temp_groups = gdf2.groupby(by=["UNIT_NAME"])[value].mean().reset_index()
    temp_groups = temp_groups.rename(columns={value:f"yearly mean {value}"})

    # merging that into the main geodataframe
    gdf2 = gdf2.merge(temp_groups)

    # plotting
    base = background_map.plot(color='grey', edgecolor="black")
    gdf2.plot(ax=base, column=f"yearly mean {value}", cmap='OrRd')

    # zooming in on the US
    base.set_xlim(-125, -65)
    base.set_ylim(25, 50)

    # the parks are too tiny and spread out to look very good


def make_corr(df, params):
    correlation = df[params].corr(numeric_only=True)
    titles = [format_text(i) for i in correlation]

    fig, axis = plt.subplots(figsize=(7,5))                              # Defining a figure and its subplots/axes
    axis.imshow(correlation)                                # Plots the inputted correlation matrix
    correl_nums = []
    for h in range(len(correlation)):                       # Iterates through the number of rows in the correlation matrix
        for i in correlation:                               # Iterates through the titles in the correlation matrix
            correl_nums.append(round(float(correlation[i].iloc[h]),
                                     2))                    # Adds to empty list "correl_nums" the values in the correlation matrix by row
    for j in range(len(correlation)):                       # Iterates through the number of rows in the correlation matrix
        for k in range(len(correlation)):                   # Iterates through the number of rows in the correlation matrix
            val = correl_nums[k + len(correlation) * j]
            if val >= .5:
                text = axis.text(x=(k-.28), y=(j+.05), s=val, fontsize=7.5,
                                 color="black")             # Adds the value (s) in the correlation matrix at coordinate (x,y) by row
            else:
                text = axis.text(x=(k-.28), y=(j+.05), s=val, fontsize=7.5)
    axis.set_xticks(range(len(titles)), labels=titles, rotation=45)             # Sets the x-axis labels based on the labels list "titles"
    axis.set_yticks(range(len(titles)), labels=titles)                          # Sets the y-axis labels based on the labels list "titles"
    axis.set_title("Weather Data per Month for National Parks in 2025")
    return fig

# def make_pie(df, params):
#     fig, ax = plt.subplots()
#     df2 = df.groupby(["UNIT_NAME"], as_index=False).agg({i: "mean" for i in params})
#     labels = params
#     size = 0.25
#     for row in range(len(df2)):
#         wedges = [abs(val) for val in df2[params].loc[row]]
#         ax.pie(wedges, radius=.5, wedgeprops=dict(width=size, edgecolor='w'))
#     plt.legend(labels, ncols=2)
#     plt.title(label="Yearly Weather Data for National Parks in 2025")
#     return fig

def make_plot(df, params):
    """Makes a lineplot for each of the given columns
    :param df: dataframe of park data (already filtered for the specific park(s))
    :param params: list of string names for attribute columns
    """
    fig, ax = plt.subplots()

    # setting a dict of parameter types to colors
    colors = {mean_t:"lawngreen", max_t:"orangered", min_t:"lightblue",
                 wind_s:"plum", wind_g:"mediumpurple", precip_col:"royalblue",
              "so2":"lightsteelblue", "pm25":"grey", "pm10":"slategray", "co":"lightgrey", "o3":"linen", "no2":"rosybrown"}

    # going through each of the attributes to plot
    for i in params:
        # going through each of the parks in that dataframe (so their separate lines don't
        # loop back to each other if there are multiple)
        j=0
        for park in df[park_col].unique():
            park_df = df[df[park_col]==park]
            color = colors[i]
            # adding labels for first occurrence of a attribute, but then not for subsequent loops
            if j<1:
                ax.plot(park_df["date_month"], park_df[i], color=color, alpha=0.5, label=format_text(i))
                j+=1
            else:
                ax.plot(park_df["date_month"], park_df[i], color=color, alpha=0.5, label="_nolegend_")
    # setting labels/legends/etc
    ax.legend(fontsize="x-small", ncols=2, loc="upper center")
    ax.set_xlabel("Month in 2025")
    ax.set_ylabel("Weather Data")
    ax.set_title(f"Weather Data per Month for National Parks in 2025")
    return fig

def make_scatter(df, params):
    fig = make_subplots()
    for val in params:
        fig.add_scatter(x=df["date_month"], y=df[val], name=format_text(val), mode="markers")
    fig.update_xaxes(title_text="Month in 2025")
    fig.update_yaxes(title_text="Weather Data")
    fig.update_layout(title="Weather Data per Month for National Parks in 2025", legend_title_text="Factors")
    return fig

def make_bar(df, params):
    fig, ax = plt.subplots()
    for i in params:
        ax.bar(df["date_month"], df[i], alpha=0.5, label=format_text(i))
    ax.legend(fontsize="x-small", ncols=2, loc="upper center")
    ax.set_xlabel("Month in 2025")
    ax.set_ylabel("Weather Data")
    ax.set_title(f"Weather Data per Month for National Parks in 2025")
    return fig

def anim_update(frame,lines,df,vals,x,y):
    """
    Takes frame, line, "vals" dictionary, x, and y
    Returns set up of values for line plot

    :param frame - int frame number
    :param lines - list of matplotlib lines to add to
    :param df - dataframe to draw from
    :param vals - list of string column names for parameters
    :param x - lits of x values
    :param y - list of list of y values
    """

    # appending the frame as the x value
    x.append(frame)
    # looping through all the attributes
    for i in range(len(vals)):
        # appending the next value of that attribute to its y value list
        y[i].append(df.loc[frame, vals[i]])
        # updating its line with the new data
        lines[i].set_data(x,y[i])
    return lines

def make_animate(df, params):
    """
    Creates animated line plots from the data in the dataframe for the given parameters
    """
    fig, ax = plt.subplots(figsize=(7,5))          # Defines figure and axes, with figure size
    ax.set_xticks([a for a in range(1,13)], df["date_month"].unique().tolist())

    # creating lists to append values into for each thing being plotted
    lines = []
    x = []
    y_lists = []

    for i in range(len(params)):
        line, = plt.plot([],[], label=params[i])
        lines.append(line)
        y_lists.append([])

    anim = FuncAnimation(fig, anim_update, frames=range(0, 12), fargs=(lines, df, params, x, y_lists),
                                                     repeat=False, interval=400)

    ax.legend()

    # setting the bounds of the plot to be at the max/min values of the numeric parameters
    # the 2 assumes the two non-numeric columns UNIT_NAME and date_month are first
    ymin = (df.min().iloc[2:]).min()
    ymax = (df.max().iloc[2:]).max()
    plt.ylim(ymin, ymax)

    anim.save("animation.mp4", writer="ffmpeg")
    return "animation.mp4"

def make_comparitive_scatter(df, attr1, attr2):
    """
    Creates a scatterplot
    :param df: the dataframe of the selected park(s) with just the specific attributes
    :param attr1: attribute for x col
    :param attr2: attribute for y col
    :return: a scatterplot
    """

    figure = px.scatter(df, x=attr1, y=attr2)

    return figure


# for testing it
def main():
    gdf = gpd.read_parquet("data/cleaned_data.parquet")

    # gdf.plot()
    # plt.show()

    create_choropleth(gdf, "mean_temp")

    plt.show()

if __name__=="__main__":
    main()
