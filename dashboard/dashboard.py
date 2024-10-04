import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

#menyiapkan helper function untuk dataframe

#menyiapkan dataset
df_hour=pd.read_csv("https://raw.githubusercontent.com/Rahmatbaaka/submission-AnalisisData_Dicoding-2024/main/dashboard/df_bike_hour.csv")
df_hour.sort_values(by="dteday")
df_hour.reset_index(inplace=True)
df_hour["dteday"]=pd.to_datetime(df_hour["dteday"])

#filter data
min_date = df_hour["dteday"].min()
max_date = df_hour["dteday"].max()

with st.sidebar:

    st.image("https://raw.githubusercontent.com/Rahmatbaaka/submission-AnalisisData_Dicoding-2024/main/dashboard/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )