import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go


def generate_color_dict_plotly(categories, colormap="Paired"):
    """
    Generate a color dictionary for given categories using a specified colormap.

    :param categories: List of category names
    :param colormap: Name of the colormap to use (default is 'Paired')
    :return: Dictionary mapping categories to colors
    """
    # if colormap in pc.sequential.__all__:
    #     colors = getattr(pc.sequential, colormap)
    # elif colormap in pc.diverging.__all__:
    #     colors = getattr(pc.diverging, colormap)
    # elif colormap in pc.qualitative.__all__:
    #     colors = getattr(pc.qualitative, colormap)
    # else:
    #     # Default to 'Plotly' if the specified colormap is not found
    #     colors = pc.qualitative.Plotly

    # Generate evenly spaced colors from the colormap
    n_colors = len(categories)
    color_scale = px.colors.sample_colorscale(colormap, n_colors, low=0.05, high=0.95)

    return dict(zip(categories, color_scale))


status = "Operação"
category = "SigTipoGeracao"
color_scale = "Viridis"
# Load the GeoJSON file of Brazilian states
geojson_file_path_state = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson"
brazil_states = gpd.read_file(geojson_file_path_state)

# read data
csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
df = pd.read_pickle(csv_file_path)


# define colors for graph
categories = df[category].unique()
color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)


# Create a color discrete map from your dictionary
color_discrete_map = {
    cat: color for cat, color in color_dict.items() if cat in categories
}

# Create the base map
fig = px.choropleth_mapbox(
    brazil_states,
    geojson=brazil_states.geometry,
    locations=brazil_states.index,
    mapbox_style="carto-positron",
    zoom=3,
    center={"lat": -15.7801, "lon": -47.9292},  # Coordinates for Brasília
    opacity=0.3,
)

# Add scatter plot for power plants
for cat in categories:
    category_data = df[df[category] == cat]
    fig.add_trace(
        go.Scattermapbox(
            lat=category_data["NumCoordNEmpreendimento"],
            lon=category_data["NumCoordEEmpreendimento"],
            mode="markers",
            marker=dict(size=5, color=color_dict[cat]),
            text=category_data["NomEmpreendimento"],
            name=cat,  # This will appear in the legend
            hoverinfo="text",
        )
    )

# Update layout
fig.update_layout(
    title="Power Plants in Brazil",
    legend_title="Power Plant Categories",
    paper_bgcolor="#343a40",
    plot_bgcolor="#343a40",
    font_color="white",
)

# Show the plot
fig.show()
