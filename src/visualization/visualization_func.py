# import libraries
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go


# define function for manage colors in graphs
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


def get_color_plotly(color_dict, categories):
    """
    Get colors for specified categories from a color dictionary.

    :param color_dict: Dictionary mapping categories to colors
    :param categories: List of categories to get colors for
    :return: List of colors for the specified categories
    """
    return [
        color_dict.get(category, "#000000") for category in categories
    ]  # Default to black if category not found


# define function for display choropleth map
def choropleth_mapbox_ele_pow(status, colors_scale):

    # read procesed data
    csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    df_aux = pd.read_pickle(csv_file_path)

    # read geojson data
    geojson_file_path_state = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson"
    geojson_data_state = gpd.read_file(geojson_file_path_state)

    # make dataframe for map
    df_sorted = (
        df_aux[df_aux["DscFaseUsina"] == status]
        .groupby("SigUFPrincipal")
        .agg({"MdaPotenciaOutorgadaKw": "sum", "MdaPotenciaFiscalizadaKw": "sum"})
        .reset_index()
    )

    # get better color for limits of the range in the color map
    key_min = np.percentile(df_sorted.MdaPotenciaOutorgadaKw, 5)
    key_max = np.percentile(df_sorted.MdaPotenciaOutorgadaKw, 95)

    # get the center of brazil to display by default
    state_bounds = geojson_data_state.geometry.total_bounds
    south, west, north, east = state_bounds

    # Calculate the center coordinates
    # center = {"lat": (south + north) / 2, "lon": (west + east) / 2}
    center = {"lat": -11.61, "lon": -51.81}
    # Calculate the zoom level
    zoom = 2  # Start with a zoom level of 4 (can be adjusted as needed)

    # create choropleth map
    fig = px.choropleth_mapbox(
        df_sorted,
        geojson=geojson_data_state,
        locations="SigUFPrincipal",
        featureidkey="properties.abbrev_state",
        color="MdaPotenciaOutorgadaKw",
        color_continuous_scale=colors_scale,
        mapbox_style="carto-positron",
        range_color=[key_min, key_max],
        center=center,
        zoom=zoom,
        opacity=0.5,
        labels={"MdaPotenciaOutorgadaKw": "Electric Power KW"},
        title=f"Electric Power by State by {status}",
    )
    fig.update_geos(fitbounds="locations", visible=False, scope="south america")

    # update layout atributes
    fig.update_layout(
        mapbox=dict(style="carto-positron"),
        paper_bgcolor="#343a40",
        plot_bgcolor="#343a40",
        font_color="white",
        legend=dict(title=dict(text="Legend Title"), orientation="h", x=1, y=1.02),
    )

    return fig


# define bar plot by status and category
def bar_plot_status_category(status, category, color_scale):

    # read data
    csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    df_aux = pd.read_pickle(csv_file_path)

    # make sorted dataframe
    df_sorted = (
        df_aux[df_aux["DscFaseUsina"] == status]
        .groupby(category)
        .agg({"MdaPotenciaOutorgadaKw": "sum", "MdaPotenciaFiscalizadaKw": "sum"})
        .reset_index()
    )
    # define colors
    # get unique values of categories
    categories = list(df_aux[category].unique())
    # get a dictionary with fix colors for each category
    color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)
    color = get_color(color_dict=color_dict, categories=categories)
    # make bar graph
    fig = px.bar(
        df_sorted,
        x=category,
        y="MdaPotenciaOutorgadaKw",
        # color_discrete_sequence=px.colors.qualitative.Alphabet,
        color=category,
        color_discrete_map=color_dict,
        title=f"Electric power by {status} and by {category}",
        labels={"x": category, "y": "Electric Power"},
    )
    fig.update_layout(
        paper_bgcolor="#343a40",
        plot_bgcolor="#343a40",
        font_color="white",
    )

    return fig


# #define pie plot by status and category
def pie_plot_status_category(status, category, color_scale):

    # read data
    csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    df_aux = pd.read_pickle(csv_file_path)

    # generate colors for graphs
    categories = list(df_aux[category].unique())
    color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)

    # make sorted dataframe
    df_sorted = (
        df_aux[df_aux["DscFaseUsina"] == status]
        .groupby(category)
        .agg({"MdaPotenciaOutorgadaKw": "sum", "MdaPotenciaFiscalizadaKw": "sum"})
        .reset_index()
    )

    # plot the pie graph
    fig = px.pie(
        df_sorted,
        values="MdaPotenciaOutorgadaKw",
        names=category,
        title=f"Electric Power by {status} and by {category}",
        color=category,
        color_discrete_map=color_dict,
    )

    fig.update_layout(
        paper_bgcolor="#343a40",
        plot_bgcolor="#343a40",
        font_color="white",
    )

    return fig


# #define historical line plot
def hist_line_plot(category, color_scale):

    # read data
    csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    df_aux = pd.read_pickle(csv_file_path)

    # generate colors for graph
    categories = df_aux[category].unique()
    color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)

    # for this graph, only take into consideration operative power plants
    df_sorted = df_aux[df_aux["DscFaseUsina"] == "Operação"]
    # get the year of the datetime column to do a groupby

    df_sorted["Year"] = df_sorted["DatEntradaOperacao"].dt.year

    # group by year and category and summ the electric power
    df_sorted = (
        df_sorted.groupby(["Year", category])["MdaPotenciaOutorgadaKw"]
        .sum()
        .reset_index()
    )
    df_sorted = df_sorted.sort_values("Year")
    # calculate cumulative sum of the power by category
    df_sorted["Cumulative_Power"] = df_sorted.groupby(category)[
        "MdaPotenciaOutorgadaKw"
    ].cumsum()

    # create a dataframe with all the years from min to max date with every category combination
    year_range = range(df_sorted["Year"].min(), df_sorted["Year"].max() + 1)
    df_all_years = pd.DataFrame(
        [(year, cat) for year in year_range for cat in categories],
        columns=["Year", category],
    )

    # merge dataframe with cumulative electric power with dataframe with all years
    df_historic = pd.merge(
        df_all_years,
        df_sorted[["Year", category, "Cumulative_Power"]],
        on=["Year", category],
        how="left",
    )

    # fill forward cumulative values to fill NaN or 0 gaps
    df_historic["Cumulative_Power"] = df_historic.groupby(category)[
        "Cumulative_Power"
    ].ffill()

    # fill any remaining NaN value with 0, specially the first values not filled before
    df_historic["Cumulative_Power"] = df_historic["Cumulative_Power"].fillna(0)

    # Create the stacked area chart
    fig = px.area(
        df_historic,
        x="Year",
        y="Cumulative_Power",
        color=category,
        labels={
            "Cumulative_Power": "Installed Power (kW)",
            category: category,
        },
        title=f"Historical Evolution of Installed Electric Power by {category}",
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Installed Power (kW)",
        legend_title=category,
        hovermode="x unified",
        paper_bgcolor="#343a40",
        plot_bgcolor="#343a40",
        font_color="white",
    )

    return fig


# define location map for every generator
def loc_map_plot(status, category, color_scale):

    # read data
    csv_file_path = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data.pkl"
    df_aux = pd.read_pickle(csv_file_path)

    # read geojson data
    geojson_file_path_state = r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson"
    geojson_data_state = gpd.read_file(geojson_file_path_state)

    # define colors for graph
    categories = df_aux[category].unique()
    color_dict = generate_color_dict_plotly(categories=categories, colormap=color_scale)

    # filter dataframe
    df_filtered = df_aux[df_aux["DscFaseUsina"] == status]

    # create colormap for points of location by category
    color_discrete_map = {
        cat: color
        for cat, color in color_dict.items()
        if cat in df_filtered[category].unique()
    }

    # Calculate the center coordinates
    center = {"lat": -11.61, "lon": -51.81}

    # Calculate the zoom level
    zoom = 2.5  # Start with a zoom level of 4 (can be adjusted as needed)

    # Create the base map
    fig = px.choropleth_mapbox(
        geojson_data_state,
        geojson=geojson_data_state.geometry,
        locations=geojson_data_state.index,
        mapbox_style="carto-positron",
        zoom=zoom,
        center=center,
        opacity=0.3,
    )

    # Add scatter plot for location points of power plants
    for cat in categories:
        category_data = df_filtered[df_filtered[category] == cat]
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

    return fig
