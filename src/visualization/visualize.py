# import libraries
import numpy as np
import pandas as pd
import plotly.express as px

# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# import matplotlib.ticker as ticker
# import geopandas as gpd

# import data procesed
df_data = pd.read_pickle(
    r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
)

# set format for numeric visuals
pd.options.display.float_format = "{0:.2f}".format

# make dataframes for graphs

# Assuming your DataFrame is called 'df' with columns: 'Date', 'Category', 'Electric-Power', 'Name'
# If it's not, replace 'df' with your actual DataFrame name

df = df_data[df_data["DscFaseUsina"] == "Operação"]
# 2. Sort the DataFrame by date
df = df.sort_values("DatEntradaOperacao")

# 3. Create a cumulative sum of 'Electric-Power' for each category
df["Cumulative_Power"] = df.groupby("SigTipoGeracao")["MdaPotenciaOutorgadaKw"].cumsum()

# 4. Create a date range from the minimum to maximum date in your data
date_range = pd.date_range(
    start=df["DatEntradaOperacao"].min(), end=df["DatEntradaOperacao"].max(), freq="D"
)

# 5. Create a new DataFrame with all dates and categories
categories = df["SigTipoGeracao"].unique()
df_all_dates = pd.DataFrame(
    [(date, cat) for date in date_range for cat in categories],
    columns=["DatEntradaOperacao", "SigTipoGeracao"],
)

# 6. Merge this with your original data
df_merged = pd.merge(
    df_all_dates,
    df[["DatEntradaOperacao", "SigTipoGeracao", "Cumulative_Power"]],
    on=["DatEntradaOperacao", "SigTipoGeracao"],
    how="left",
)

# 7. Forward fill the cumulative power values
df_merged["Cumulative_Power"] = df_merged.groupby("SigTipoGeracao")[
    "Cumulative_Power"
].ffill()

# 8. Fill any remaining NaN values with 0
df_merged["Cumulative_Power"] = df_merged["Cumulative_Power"].fillna(0)

# 9. Create the stacked area chart
fig = px.area(
    df_merged,
    x="DatEntradaOperacao",
    y="Cumulative_Power",
    color="SigTipoGeracao",
    labels={
        "Cumulative_Power": "Cumulative Installed Power",
        "SigTipoGeracao": "Power Plant Category",
    },
    title="Historical Evolution of Cumulative Installed Electric Power in Brazil by Category",
)

# 10. Customize the layout
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Cumulative Installed Power",
    legend_title="SigTipoGeracao",
    hovermode="x unified",
)

# 11. Show the plot
fig.show()
