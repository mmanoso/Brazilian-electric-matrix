# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
import geopandas as gpd

# import data procesed
df_data = pd.read_pickle("../../data/processed/transformed_data.pkl")

# set format for numeric visuals
pd.options.display.float_format = "{0:.2f}".format

# make dataframes for graphs
