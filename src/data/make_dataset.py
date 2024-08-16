# import libraries
import numpy as np
import pandas as pd
from geobr import read_state

# import data to pandas dataframe
df_raw_data = pd.read_csv(
    r"../../data/raw/siga-empreendimentos-geracao.csv",
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

# import shapes of brazilian states for later ploting maps
df_brazlian_states = read_state(code_state="all")

# merge brazilian states using the abreviation of states as key binding
df_data = pd.merge(
    df_brazlian_states,
    df_data,
    left_on="abbrev_state",
    right_on="SigUFPrincipal",
    how="left",
)
df_data = df_data.drop(columns=["code_state", "abbrev_state", "code_region"])

# check null values
df_data.isnull().any()

df_data.to_pickle("../../data/processed/transformed_data.pkl")
