# import libraries
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html, dcc, Input, Output, Dash

# read transformed data
# df_data = pd.read_pickle("../../data/processed/transformed_data.pkl")

# obtain unique values for dropdown
# dropdown_values = {"operative_state": [df_data["DscFaseUsina"].unique()]}
dropdown_values = {
    "regions": ["North East", "South East"],
    "year": [2012, 2013, 2014, 2015],
}
# create Dash aplication
app = Dash(__name__)

# define app layout
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="regions-dropdown",
            options=[
                {"label": region, "value": region}
                for region in dropdown_values["regions"]
            ],
            value="North East",
        ),
        html.Div([dcc.Graph(id="plot1"), dcc.Graph(id="plot2")]),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
