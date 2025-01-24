import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_registered_df(df):
    registered_df = df.resample(rule='M', on='dtedaye').agg({
        "registered_y": "sum"
    })
    registered_df = registered_df.reset_index()
    registered_df.rename(columns={
        "registered_y": "daftar rental"
    }, inplace=True)
    
    return registered_df

def create_bymnth_df(df):
    bymnth_df = df.groupby(by="mnth").season.nunique().reset_index()
    bymnth_df.rename(columns={
        "season": "Musim"
    }, inplace=True)
    
    return bymnth_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="mnth", as_index=False).agg({
        "dteday": "max",
        "weathersit_x": "nunique", #mengambil data cuaca
        "season_x": "nunique",
    })
    rfm_df.columns = ["mnth","tanggal", "weathersit", "season"]
    
    return rfm_df

# Load berkas all_data
all_df = pd.read_csv("all_data.csv")


date = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in date:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/ilhamarifinsamsul/final-project-analisis-data/raw/main/asset/bike.png", width=100)
