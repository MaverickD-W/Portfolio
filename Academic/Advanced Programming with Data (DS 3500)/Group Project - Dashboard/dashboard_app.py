
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import panel as pn
from matplotlib.animation import FuncAnimation
from plotly.subplots import make_subplots

from dashboard_api import ParkDash
import dashboard_viz as viz

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

data = ParkDash(data_path)

def format_text(text):
    """replaces underscores with spaces and converts to title case"""
    return (" ").join((text).split("_")).title()

def call_data(park, params, aq_cols):
    """returns monthly averages of a subset of the data"""
    global data
    params_og = [a.replace(" ", "_").lower() for a in params]
    if len(aq_cols) != 0:
        params_og = params_og + aq_cols
    df = data.get_avg(params_og, park)
    return pn.pane.DataFrame(df)

def call_plot(park, params, aq_cols, plot):
    global data
    params_og = [a.replace(" ", "_").lower() for a in params]
    if len(aq_cols) != 0:
        params_og = params_og + aq_cols
    df = data.get_avg(params_og, park)

    if plot == "Scatter Plot":
        fig = viz.make_scatter(df, params_og)
    if plot == "Line Plot":
        fig = viz.make_plot(df, params_og)
    if plot == "Bar Chart":
        fig = viz.make_bar(df, params_og)
    if plot == "Correlation Matrix":
        fig = viz.make_corr(df, params_og)
    return fig

def call_animation(park, params, aq_cols):
    global data
    params_og = [a.replace(" ", "_").lower() for a in params]
    if len(aq_cols) != 0:
        params_og = params_og + aq_cols
    df = data.get_avg(params_og, park)
    anim = viz.make_animate(df, params_og)

    video = pn.pane.Video(anim, width=640, loop=False, autoplay=True)

    #return anim
    return video

def call_comparison(park, attr1, attr2):
    global data
    attr1 = attr1.replace(" ", "_").lower()
    attr2 = attr2.replace(" ", "_").lower()

    df = data.get_subset(parks=park, params=[attr1, attr2])

    fig = viz.make_comparitive_scatter(df, attr1, attr2)

    return fig


def main():

    pn.extension()
    global data

    park_opt = pn.widgets.Select(name="National Parks", options=["All"] + data.get_parks())
    factor_names = [format_text(a) for a in factor_cols]
    factors_slct = pn.widgets.MultiChoice(name="Weather Features", options=factor_names, value=factor_names[:3])
    aq_slct = pn.widgets.MultiChoice(name="Air Quality Features", options=aq_names, value=[])
    viz_opts = pn.widgets.RadioBoxGroup(name="Visualizations", options=["Scatter Plot", "Line Plot", "Correlation Matrix", "Bar Chart"], value="Scatter Plot")
    # month_sldr = pn.widgets.IntSlider(name="Month", start=1, end=12, step=1, value=1)

    x_slct = pn.widgets.Select(options=factor_names+aq_names, name="x-Axis Attribute", value="Mean Temp")
    y_slct = pn.widgets.Select(options=factor_names+aq_names, name="y-Axis Attribute", value="Wind Speed")

    dataset = pn.bind(call_data, park_opt, factors_slct, aq_slct)
    plot = pn.bind(call_plot, park_opt, factors_slct, aq_slct, viz_opts)
    anim = pn.bind(call_animation, park_opt, factors_slct, aq_slct)
    comparison_scatter = pn.bind(call_comparison, park_opt, x_slct, y_slct)

    srch_lgnd = pn.Card(pn.Column(park_opt, factors_slct, aq_slct), title="Filters", collapsed=False, width=335)
    vis_lgnd = pn.Card(pn.Column(viz_opts), title="Static Visualization Type", collapsed=False, width=335)
    comp_lgnd = pn.Card(pn.Column(x_slct, y_slct), title="Comparitive Scatterplot Selections", collapsed=False, width=335)
    # plt_lgnd = pn.Card(pn.Column(), title="Plot", collapsed=True)

    layout = pn.template.FastListTemplate(title="National Park Weather & Air Quality 2025",
                            sidebar=[srch_lgnd, vis_lgnd, comp_lgnd],
                            main=[pn.Tabs(("Dataset", pn.panel(dataset, loading_indicator=True)),
                                            ("Static Visualizations", pn.panel(plot, loading_indicator=True)),
                                            ("Animation", pn.panel(anim, loading_indicator=True)),
                                            ("Compare Two Attributes", pn.panel(comparison_scatter, loading_indicator=True)),
                                            active=1)],
                            theme_toggle=False,
                            accent="#2E7E43",
                            neutral_color="#ECBA82",
                            background_color="#FFE8CD"
                ).servable()

    layout.show()

main()
