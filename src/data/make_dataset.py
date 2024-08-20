# import libraries
import numpy as np
import pandas as pd
import geopandas as gpd
import geobr
from geobr import read_state

# import data to pandas dataframe
df_raw_data = pd.read_csv(
    r"C:\Users\Mariano\Documents\Aprendizaje Data Science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\raw\siga-empreendimentos-geracao.csv",
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


# import shapefiles and convert to geoJSON
myshpfile = read_state(code_state="all")
myshpfile.to_file(
    r"C:\Users\Mariano\Documents\Aprendizaje Data Science\repositorio-brazilian-electric-matrix\Brazilian-electric-matrix\data\processed\all_states.geojson",
    driver="GeoJSON",
)


df_data.to_pickle("../../data/processed/transformed_data.pkl")

#
