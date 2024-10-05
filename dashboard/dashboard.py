import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon=":bar_chart:", layout="wide")

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

#filter data
min_date = df_hour["dteday"].min()
max_date = df_hour["dteday"].max()

#membuat sidebar untuk logo dan input date
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

#membuat dataframe untuk visualisasi
cuaca_df = create_cuaca_df(main_df)
workday_holiday_df = create_workday_holiday_df(main_df)
total_2012_df = create_total_2012_df(main_df)
hourly_usage_df = create_hourly_usage_df(main_df)

#membuat header dashboard
st.header('Bike Sharing Dashborad 🚲')
st.markdown("""---""")

#jumblah berdasarkan pengaruh cuaca
st.subheader('Cuaca Bike Sharing')

col1, col2, col3, col4= st.columns(4)

with col1:
    total_clear = main_df[main_df["weathersit"] == 'Clear']['cnt'].sum()
    st.metric("Total Pengguna clear", value=total_clear )

with col2:
    total_cloudy  = main_df[main_df["weathersit"] == 'Cloudy']['cnt'].sum()
    st.metric("Total Pengguna Cloudy", value=total_cloudy )

with col3:
    total_rain  = main_df[main_df["weathersit"] == 'Rain']['cnt'].sum()
    st.metric("Total Pengguna Rain", value=total_rain )

with col4:
    total_heavy_rain  = main_df[main_df["weathersit"] == 'Heavy Rain']['cnt'].sum()
    st.metric("Total Pengguna Heavy Rain", value=total_heavy_rain )

#persiapan data untuk pengaruh cuaca
cuaca_df.columns = ['cnt']
cuaca_df = cuaca_df.reset_index()

#membuat bar plot berdasarkan pengaruh cuaca
fig, ax = plt.subplots(figsize=(10, 6))  
fig.patch.set_facecolor('none')
ax.patch.set_alpha(0)

sns.barplot(data=cuaca_df,
            x='weathersit',
            y='cnt',
            ax=ax,
            palette='Blues_d'  
            ) 

ax.set_title('Jumlah Pengguna Berdasarkan Kategori Cuaca', color='white')
ax.set_xlabel('Kategori Cuaca', color='white')
ax.set_ylabel('Jumlah Pengguna', color='white')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, color='white')  
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_color('none')  
ax.spines['right'].set_color('none')
ax.tick_params(colors='white')

plt.tight_layout()  
st.pyplot(fig)

#rata2 harian hari kerja vs hari libur
st.subheader(' Workingday & Holiday Bike Sharing')

col1, col2= st.columns(2)

with col1:
    mean_workinday = main_df[(main_df['workingday'] == 1) & (main_df["yr"] == 2012)]['cnt'].mean().round() * 24
    st.metric("Rata-rata pengguna hari kerja", value=mean_workinday )

with col2:
    mean_holiday = main_df[(main_df['holiday'] == 1) & (main_df["yr"] == 2012)]['cnt'].mean().round() * 24
    st.metric("Rata-rata pengguna hari libur", value=mean_holiday )

labels = ['Hari Kerja', 'Hari Libur']
avg_users = workday_holiday_df
colors = ['#17becf', '#ff6347']

#membuat pie chart bedasarkan mean hari kerja vs hari libur
fig, ax = plt.subplots(figsize=(7, 7))  
fig.patch.set_facecolor('none')
ax.patch.set_alpha(0)

ax.pie(avg_users, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True, textprops={'color':"white"})
ax.set_title('Perbandingan Rata-rata Pengguna pada Hari Kerja vs Hari Libur', color='white')
ax.axis('equal')  

st.pyplot(fig)

#pengguna bulanan 2012
st.subheader('month in 2012 Bike Sharing')
sorted_df = total_2012_df.sort_values(by='cnt', ascending=False)

# Mendapatkan 3 tertinggi dan 3 terendah
top_indices = sorted_df.head(3).index
bottom_indices = sorted_df.tail(3).index

# Menentukan warna
colors = ['blue' if index in top_indices else 'orange' if index in bottom_indices else 'grey' for index in total_2012_df.index]

#membuat bar plot pengguna bulanan 2012
fig, ax = plt.subplots(figsize=(15, 6))
fig.patch.set_facecolor('none')
ax.patch.set_alpha(0)

sns.barplot(total_2012_df,
            x='mnth',
            y='cnt',
            hue='mnth',
            palette=colors,
            ax=ax)

ax.set_title('Jumlah Pengguna Berdasarkan Bulan (2012)', color='white')
ax.set_xlabel('Bulan', color='white')
ax.set_ylabel('Jumlah Pengguna', color='white')
ticks = range(len(ax.get_xticklabels()))  
ax.set_xticks(ticks)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, color='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_color('none')  
ax.spines['right'].set_color('none')
ax.tick_params(colors='white')

plt.tight_layout()
st.pyplot(fig)

#clustering berdasarkan jam
st.subheader('Clustring Hourly Bike Sharing')

#membuat barplot berdasasarkan clustering pengguna setiap jam
fig, ax = plt.subplots(figsize=(16, 6))
fig.patch.set_facecolor('none')
ax.patch.set_alpha(0)

sns.barplot(data=hourly_usage_df, x='hr', y='cnt', hue='Cluster', ax=ax)
ax.set_title('Penggunaan Sepeda Berdasarkan Jam', fontsize=16, color='white')
ax.set_xlabel('Jam', fontsize=14, color='white')
ax.set_ylabel('Jumlah Pengguna', fontsize=14, color='white')
ax.set_xticks(ticks=range(0, 24))
ax.set_xticklabels([f"{hr}:00" for hr in range(24)], fontsize=12, color='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_color('none')  
ax.spines['right'].set_color('none')
ax.tick_params(colors='white')
ax.legend(title='Cluster', fontsize=12, title_fontsize='13', facecolor='none', edgecolor='none', labelcolor='white')

plt.tight_layout()
st.pyplot(fig)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            header {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
