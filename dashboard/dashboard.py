import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon=":bar_chart:", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#menyiapkan helper function untuk dataframe

def create_cuaca_df(df):
    faktor_cuaca_df = df[['weathersit', 'cnt']].groupby(by='weathersit').agg({
        "cnt":['sum']
    }).sort_values(("cnt", "sum"), ascending=False)
    return faktor_cuaca_df

def create_workday_holiday_df(df):
    workingday_data = df[(df['workingday'] == 1) & (df["yr"] == 2012)]
    holiday_data = df[(df['holiday'] == 1) & (df["yr"] == 2012)]
    avg_workingday_users = workingday_data['cnt'].mean()
    avg_holiday_users = holiday_data['cnt'].mean()
    return [avg_workingday_users, avg_holiday_users]

def create_total_2012_df(df):
    df_yr2012 = df[df["yr"] == 2012]
    df_yr2012 = df_yr2012[['yr', 'mnth', 'cnt']]
    df_yr2012 = df_yr2012.groupby(by=["mnth"]).agg({
        'cnt': ["sum"]
    })

    df_yr2012.columns = ['cnt']
    df_yr2012 = df_yr2012.reset_index()

    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_yr2012['mnth'] = pd.Categorical(df_yr2012['mnth'], categories=months_order, ordered=True)
    df_yr2012 = df_yr2012.sort_values('mnth').reset_index(drop=True)
    return df_yr2012

def create_hourly_usage_df(df):
    hourly_usage = df.groupby('hr')['cnt'].sum().reset_index()
    hourly_usage['Cluster'] = ['Morning' if hr < 12 else 'Afternoon' for hr in hourly_usage['hr']]
    return hourly_usage

#menyiapkan dataset
df_hour=pd.read_csv("https://raw.githubusercontent.com/Rahmatbaaka/submission-AnalisisData_Dicoding-2024/main/dashboard/df_bike_hour.csv")
df_hour.sort_values(by="dteday")
df_hour.reset_index(inplace=True)
df_hour["dteday"]=pd.to_datetime(df_hour["dteday"])

df_day=pd.read_csv("https://raw.githubusercontent.com/Rahmatbaaka/submission-AnalisisData_Dicoding-2024/main/dashboard/df_bike_day.csv")
df_day.sort_values(by="dteday")
df_day.reset_index(inplace=True)
df_day["dteday"]=pd.to_datetime(df_day["dteday"])

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

main_df = df_hour[(df_hour["dteday"] >= str(start_date)) &
                  (df_hour['dteday'] <= str(end_date))]

cuaca_df = create_cuaca_df(main_df)
workday_holiday_df = create_workday_holiday_df(main_df)
total_2012_df = create_total_2012_df(main_df)
hourly_usage_df = create_hourly_usage_df(main_df)

#membuat header dashboard
st.header('Bike Sharing Dashborad 🚲')

st.subheader('Cuaca Bike Sharing')

cuaca_df.columns = ['cnt']
cuaca_df = cuaca_df.reset_index()

fig, ax = plt.subplots(figsize=(10, 6))  

sns.barplot(data=cuaca_df,
            x='weathersit',
            y='cnt',
            ) 

ax.set_title('Jumlah Pengguna Berdasarkan Kategori Cuaca')
ax.set_xlabel('Kategori Cuaca')
ax.set_ylabel('Jumlah Pengguna')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)  
plt.tight_layout()  

st.pyplot(fig)

st.subheader(' Workingday & Holiday Bike Sharing')

# Data untuk plotting
labels = ['Hari Kerja', 'Hari Libur']
avg_users = workday_holiday_df
colors = ['#17becf', '#ff6347']

# Membuat pie chart
fig, ax = plt.subplots(figsize=(7, 7))  

ax.pie(avg_users, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True)
ax.set_title('Perbandingan Rata-rata Pengguna pada Hari Kerja vs Hari Libur')
ax.axis('equal')  

st.pyplot(fig)

st.subheader('month in 2012 Bike Sharing')

sorted_df = total_2012_df.sort_values(by='cnt', ascending=False)

# Mendapatkan 3 tertinggi dan 3 terendah
top_indices = sorted_df.head(3).index
bottom_indices = sorted_df.tail(3).index

# Menentukan warna
colors = []
for index in total_2012_df.index:
    if index in top_indices:
        colors.append('blue')
    elif index in bottom_indices:
        colors.append('orange')
    else:
        colors.append('grey')

fig, ax = plt.subplots(figsize=(15, 6))

# Visualisasi data
sns.barplot(total_2012_df,
            x='mnth',
            y='cnt',
            hue = 'mnth',
            palette=colors,
            ax=ax)

ax.set_title('Jumlah Pengguna Berdasarkan Bulan (2012)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Pengguna')
ticks = range(len(ax.get_xticklabels()))  
ax.set_xticks(ticks)  
ax.set_xticklabels(ax.get_xticklabels(), rotation=45) 

plt.tight_layout()

st.pyplot(fig)

st.subheader('Clustring Hourly Bike Sharing')

fig, ax = plt.subplots(figsize=(16, 6))

# Membuat bar plot
sns.barplot(data=hourly_usage_df, x='hr', y='cnt', hue='Cluster', ax=ax)

# Menambahkan detail visual
ax.set_title('Penggunaan Sepeda Berdasarkan Jam', fontsize=16)
ax.set_xlabel('Jam', fontsize=14)
ax.set_ylabel('Jumlah Pengguna', fontsize=14)

# Mengatur format label jam
ax.set_xticks(ticks=range(0, 24))
ax.set_xticklabels([f"{hr}:00" for hr in range(24)], fontsize=12)

# Menambahkan legenda
ax.legend(title='Cluster', fontsize=12)
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(fig)