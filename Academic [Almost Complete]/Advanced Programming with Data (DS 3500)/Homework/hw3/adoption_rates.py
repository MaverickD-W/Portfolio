import pandas as pd
import plotly.graph_objects as go
import panel as pn

filepaths = ["Children_Adopted.csv", "Children_Entering_Foster_Care.csv", "Children_Exiting_Foster_Care.csv",
             "Children_in_Foster_Care.csv", "Children_Served_in_Foster_Care.csv", "Children_Waiting_for_Adoption.csv"]            # Define csv filepaths
state_col = "State"
adopt_col = "Children_Adopted"
enter_care = "Children_Entering_Foster_Care"
exit_care = "Children_Exiting_Foster_Care"
in_care = "Children_in_Foster_Care"
ser_in_care = "Children_Served_in_Foster_Care"
wait_adopt = "Children_Waiting_for_Adoption"

numerator = adopt_col                       # Define numerator used to get adoption proportion ("Percent_of_Children_Adopted")
denominator = in_care                       # Define denominator used to get adoption proportion ("Percent_of_Children_Adopted")
adopt_prop = "Percent_of_Children_Adopted"

params = [adopt_col, enter_care, exit_care, in_care, ser_in_care, wait_adopt]     # Define list of parameter options

crit_cols = [state_col, adopt_col]          # Define critical columns
imput_cols = params                         # Define imputable columns

bin_specs = {adopt_col: {"bins": [0, .25, .5, .75, 1],
                         "labels": ["Low Volume", "L-Medium Volume", "H-Medium Volume", "High Volume"]},
              enter_care: {"bins": [0, .25, .5, .75, 1],
                           "labels": ["Low Input", "L-Medium Input", "H-Medium Input", "High Input"]},
              exit_care: {"bins": [0, .25, .5, .75, 1],
                          "labels": ["Low Output", "L-Medium Output", "H-Medium Output", "High Output"]},
              in_care: {"bins": [0, .25, .5, .75, 1],
                         "labels": ["Low Volume", "L-Medium Volume", "H-Medium Volume", "High Volume"]},
              ser_in_care: {"bins": [0, .25, .5, .75, 1],
                         "labels": ["Low Volume", "L-Medium Volume", "H-Medium Volume", "High Volume"]},
              wait_adopt: {"bins": [0, .25, .5, .75, 1],
                         "labels": ["Low Volume", "L-Medium Volume", "H-Medium Volume", "High Volume"]}
             }         # Define bin values and bin labels

lgnd_wdth = 325                   # Define the width of the app search legend/card




class AdoptAPI:
  """
  Define class AdoptAPI for api functions
  """

  def __init__(self, filepath_lst):
    """
    Takes self and a list of csv filepaths
    Creates DataFrame from csv filepaths, concatting each csv into one row and adding an additional row for years
    """
    main_df = pd.DataFrame()                                                    # Creates and defines a blank DataFrame
    for a in range(len(filepath_lst)):                                          # Iterates through the number 'a' of filepaths (csvs)
      df = pd.read_csv(filepath_lst[a], skiprows=7, nrows=51)                   # Defines csv 'a' as a DataFrame
      col = filepath_lst[a].split(".")[0]                                       # Defines col as the csv name without ".csv"
      new_col = pd.concat([df[col] for col in df if col != "State"])            # Defines new_col as the concat of columns other than "State" in "df"
      main_df.insert(a, col, new_col)                                           # Names and inserts the concatted column into "main_df"
    years = [yr for yr in df if yr != "State" for b in range(len(df))]          # Defines list of years with each year in df being repeated for the original number of rows
    new_state = pd.concat([df["State"] for state in range(df.shape[1]-1)])      # Defines a new "State" column as the concat of "State" for the number of other rows
    main_df.insert(0, "Year", years)                                            # Names and inserts "years" list into "main_df"
    main_df.insert(0, "State", new_state)                                       # Names and inserts concatted "State" column into "main_df"
    main_df.index = range(len(main_df))                                         # Reindexes "main_df"
    self.adopt_df = main_df                                                     # Redefines "main_df" as the self.adopt_df DataFrame


  def get_proportions(self, col_num=numerator, col_denom=denominator, new_col=adopt_prop):
    """
    Takes self, column name for the numerator and one for the denominator, the new proportion column name
    Inserts a column of proportions (from col_num/col_denom) into the DataFrame
    """
    ratio = self.adopt_df[col_num]/self.adopt_df[col_denom]                 # Defines the ratio from the DataFrame numerator/denominator
    perc = round((ratio*100),2)                                             # Converts the proportion to a percentage and rounds to two decimals
    self.adopt_df.insert(len(self.adopt_df.transpose()),
                         value=(perc.to_list()), column=new_col)            # Names and inserts the proportion column at the end of "adopt_df" DataFrame

  def clean_and_bin_data(self, critical_cols=crit_cols, imput_columns=imput_cols, bin_vals=bin_specs):
    """
    Takes self, critical column names, imputable column names, and bin specs
    Cleans and bins the DataFrame
    """
    self.adopt_df.dropna(subset=critical_cols)             # Drops critical column values if there are any NA
    # self.adopt_df.fillna(-1)                             # Replaces NA values in any of the columns with -1
    self.adopt_df.drop_duplicates()                        # Drops duplicates from the Dat
    self.adopt_df[(critical_cols[1]+"_rank")] = pd.qcut(self.adopt_df[critical_cols[1]], 4,
                                                        labels=(bin_vals[critical_cols[1]]["labels"]))      # Adds column of binned values for params with a quantile cut
    for c in imput_columns:                                                     # Iterates through the imputable columns
      self.adopt_df[(c+"_rank")] = pd.qcut(self.adopt_df[c], 4,
                                           labels=(bin_vals[c]["labels"]))     # Adds a column of binned values for each imputable column with a quantile cut (4)

  def get_states(self):
    """
    Takes self
    Gets a list of unique, sorted states from the DataFrame "State" column
    """
    self.adopt_df.sort_values(by=[state_col])                       # Sorts the DataFrame values by state
    state_vals = self.adopt_df[state_col].unique().tolist()         # Defines a list of the unique sorted states (and the District of Columbia (D.C.))
    return sorted(state_vals)

  def get_subset(self, state="States & D.C.", prop_min=0):
    """
    Takes self, the state chosen from the dropdown, and the minimum adoption percentage/proportion
    Converts the self DataFrame into a subset based on state and minimum proportion values
    """
    sub = self.adopt_df.copy()
    if state != "States & D.C.":
      filter = (sub["State"] == state) & (sub[adopt_prop] >= prop_min)    # Defines filter of state and proportion for the DataFrame
    else:
      filter = (sub[adopt_prop] >= prop_min)                                        # Defines filter of proportion for the DataFrame
    sub = sub[filter]                                                     # Redefines the DataFrame based on the filter
    return sub

  def get_flow(self, state="States & D.C.", layers=params, prop_min=0):
    """
    Takes self, the state chosen from the dropdown, left layer, right layer, and min adoption proportion
    Creates a DataFrame with a grouped count to use in sankey diagram
    """
    df = self.get_subset(state, prop_min)                                      # Retrieves a subset of the self DataFrame
    new_df = df.groupby(by=[(layers[0]+"_rank"), (layers[1]+"_rank")],
                              as_index=False, observed=False, dropna=True).size()         # Defines a DataFrame of the self df grouped by the left and right layers
    new_df = new_df.rename(columns={(layers[0]+"_rank"): layers[0],
                                    (layers[1]+"_rank"): layers[1], "size": "count"})     # Renames the "new_df" columns
    return new_df


def code_map(df, vals):
  lbls = pd.concat([df[vals[0]], df[vals[1]]]).unique()
  mapped = {}
  for d in range(len(lbls)):
    mapped[lbls[d]] = d
  df[vals[0]] = df[vals[0]].map(lambda x: mapped[x])
  df[vals[1]] = df[vals[1]].map(lambda x: mapped[x])
  return df, mapped

def make_sankey(df, vals, **kwargs):
  df, mapping = code_map(df,vals)
  width = kwargs.get("width", 500)
  height = kwargs.get("height", 500)
  node = {"label": list(mapping.keys())}
  link = {"source": df[vals[0]], "target": df[vals[1]],
          "value": df["count"]}
  fig = go.Figure(go.Sankey(link=link, node=node))
  fig.update_layout(width=width, height=height, autosize=False)
  fig.update_layout(title=f"Volume of {txt_format(vals[0])} to {txt_format(vals[1])}")
  return fig


def call_data(state, adopt_proportion):
  global data
  df = data.get_subset(state, adopt_proportion)
  return pn.pane.DataFrame(df)

def call_plot(state, layers, adopt_proportion, height, width):
  global data
  while len(layers) == 1:
    layers += layers[0]
  while len(layers) == 0:
    layers = params[0:2]
  layer_og = [a.replace(" ", "_") for a in layers]
  df = data.get_flow(state, layer_og, adopt_proportion)
  fig = make_sankey(df, layer_og, height=height, width=width)
  return fig

def txt_format(text):
  return (" ").join((text).split("_"))




def main():

  pn.extension()
  global data

  data = AdoptAPI(filepaths)
  data.clean_and_bin_data()
  data.get_proportions()


  state_opt = pn.widgets.Select(name="State", options=["States & D.C."]+data.get_states())
  prop_sldr = pn.widgets.IntSlider(name="Minimum Adoption Proportion/Percentage",
                                   start=0, end=100, step=1, value=0)
  param_format = [txt_format(f) for f in params]
  param_slct = pn.widgets.MultiChoice(options=param_format, max_items=2, value=param_format[0:2])
  # param_slct = pn.Column(*(pn.widgets.Button(name=param) for param in param_format))

  height_sldr = pn.widgets.IntSlider(name="Height", start=500, end=700, step=200, value=500)
  width_sldr = pn.widgets.IntSlider(name="Width", start=750, end=1150, step=200, value=750)

  dataset = pn.bind(call_data, state_opt, prop_sldr)
  plot = pn.bind(call_plot, state_opt, param_slct, prop_sldr, height_sldr, width_sldr)

  srch_lgnd = pn.Card(pn.Column(state_opt, prop_sldr, param_slct), title="Legend", width=lgnd_wdth, collapsed=False)
  plt_lgnd = pn.Card(pn.Column(height_sldr, width_sldr), title="Plot", width=lgnd_wdth, collapsed=False)

  layout = pn.template.FastListTemplate(title="Interactive Adoption Data Dashboard",
                                        sidebar=[srch_lgnd, plt_lgnd], main=[pn.Tabs(("Dataset", dataset),
                                                                                     ("Visualization", plot),
                                                                                     active=1)], theme_toggle=False, header_background="green"
                                                                                     ).servable()
  layout.show()


if __name__ == "__main__":
  main()