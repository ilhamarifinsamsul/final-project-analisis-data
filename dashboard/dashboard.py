import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_registered_df(df):
    registered_df = df.resample(rule='M', on='dteday').agg({
        "registered_y": "sum"
    })
    registered_df = registered_df.reset_index()
    registered_df.rename(columns={
        "registered_y": "daftar_rental"
    }, inplace=True)
    
    return registered_df

def create_bymnth_df(df):
    bymnth_df = df.groupby(by="dteday").mnth_x.nunique().reset_index()
    bymnth_df.rename(columns={
        "mnth_x": "bulan",
    }, inplace=True)
    
    return bymnth_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="dteday", as_index=False).agg({
        "weathersit_x": "nunique", #mengambil data cuaca
        "season_x": "nunique",
    })
    rfm_df.columns = ["dteday", "weathersit", "season"]
    
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
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]

registered_df = create_registered_df(main_df)
bymnth_df = create_bymnth_df(main_df)
rfm_df = create_rfm_df(main_df)
    
    
st.header('Ilham Bike :sparkles:')

st.subheader('Register')

col1, col2 = st.columns(2)

with col1:
    total_regis = registered_df.daftar_rental.sum()
    st.metric("Total Registrasi", value=total_regis)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    registered_df["dteday"],
    registered_df["daftar_rental"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.subheader("Rent Demographic")

col1, col2 = st.columns(2)

with col1:
    total_mnth = bymnth_df.bulan.sum()
    st.metric("Berdasarkan Pengguna per bulan", value=total_mnth)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    bymnth_df["dteday"],
    bymnth_df["bulan"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.subheader("Rent Demographic")

col1, col2 = st.columns(2)

with col1:
    total_rfn = rfm_df.season.sum()
    st.metric("Berdasarkan Pengguna per cuaca", value=total_rfn)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    rfm_df["dteday"],
    rfm_df["season"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)