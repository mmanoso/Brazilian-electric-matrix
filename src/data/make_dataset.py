# import libraries
import numpy as np
import pandas as pd
import geopandas as gpd

# import geobr
# from geobr import read_state, read_country

# import data to pandas dataframe
df_raw_data = pd.read_csv(
    r"https://github.com/mmanoso/Brazilian-electric-matrix/blob/main/data/raw/siga-empreendimentos-geracao.csv?raw=true",
    sep=";",
    encoding="iso-8859-1",
)

# drop unused columns of raw data
df_data = df_raw_data.drop(
    columns=[
        "DatGeracaoConjuntoDados",
        "IdeNucleoCEG",
        "CodCEG",
        "DscTipoOutorga",
        "IdcGeracaoQualificada",
        "DatInicioVigencia",
        "DatFimVigencia",
        "DscPropriRegimePariticipacao",
        "DscSubBacia",
    ]
)

# change column type to datetype for DatEntradaOperacao
df_data["DatEntradaOperacao"] = pd.to_datetime(df_data["DatEntradaOperacao"])

# change columns of electric power to float type
df_data["MdaPotenciaOutorgadaKw"] = (
    df_data["MdaPotenciaOutorgadaKw"].str.replace(",", ".").astype(float)
)
df_data["MdaGarantiaFisicaKw"] = (
    df_data["MdaGarantiaFisicaKw"].str.replace(",", ".").astype(float)
)
df_data["NumCoordNEmpreendimento"] = (
    df_data["NumCoordNEmpreendimento"].str.replace(",", ".").astype(float)
)
df_data["NumCoordEEmpreendimento"] = (
    df_data["NumCoordEEmpreendimento"].str.replace(",", ".").astype(float)
)

# change column names to english
df_data.rename(
    columns={
        "DscFaseUsina": "status",
        "DscOrigemCombustivel": "fuel_origin",
        "DscFonteCombustivel": "fuel_type",
        "NomFonteCombustivel": "fuel_type_name",
        "SigTipoGeracao": "generator_type",
        "SigUFPrincipal": "states",
        "NumCoordNEmpreendimento": "latitude",
        "NumCoordEEmpreendimento": "longitude",
        "MdaPotenciaFiscalizadaKw": "electric_power_decl",
        "MdaPotenciaOutorgadaKw": "electric_power_inst",
    },
    inplace=True,
)
# # import shapefiles and convert to geoJSON
# myshpfile = read_state(code_state="all")
# myshpfile.to_file(
#     r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson",
#     driver="GeoJSON",
# )
# countryshpfile = read_country(year=2020)
# countryshpfile.to_file(
#     r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\brazil_country.geojson",
#     driver="GeoJSON",
# )

df_data.to_pickle(
    r"C:\Users\Mariano\Documents\aprendizaje-data-science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\transformed_data_app.pkl"
)

#
