import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


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
    bymnth_df = df.groupby(by="dteday").mnth_x.sum().sort_values(ascending=False).reset_index()

    return bymnth_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="dteday").season_x.sum().sort_values(ascending=False).reset_index()

    return byseason_df


def create_weekday_df(df):
    weekday_df = df.resample(rule='M', on='dteday').agg({
        "weekday_x": "sum"
    })
    weekday_df = weekday_df.reset_index()
    weekday_df.rename(columns={
        "weekday_x": "rent_weekday"
    }, inplace=True)
    
    return weekday_df



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
byweekday = create_weekday_df(main_df)
byseason = create_byseason_df(main_df)
    
    
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


st.subheader("Best Rental Berdasarkan Bulan")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="mnth_x", y="dteday", data=bymnth_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Rent:", fontsize=30)
ax[0].set_title("Best Rent Per Bulan", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="mnth_x", y="dteday", data=bymnth_df.sort_values(by="mnth_x", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Rent", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Best Rent Per Bulan", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.subheader("Best Rental Berdasarkan Season")

byseason_df = all_df.groupby(by="dteday").season_x.sum().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="season_x", y="dteday", data=byseason_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Rent:", fontsize=30)
ax[0].set_title("Best Rent Per Season", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="season_x", y="dteday", data=byseason_df.sort_values(by="season_x", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Rent", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Best Rent Per Season", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)


st.subheader('Pengguna per Weekday')

col1, col2 = st.columns(2)

with col1:
    total_week = byweekday.rent_weekday.sum()
    st.metric("Weekday", value=total_week)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    byweekday["dteday"],
    byweekday["rent_weekday"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.caption('Copyright (c) Ilham Arifin 2024')