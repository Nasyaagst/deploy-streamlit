
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import streamlit as st

df = pd.read_csv("https://raw.githubusercontent.com/Nasyaagst/Submission/main/all_data.csv")

max_pm25 = df[df['PM2.5'] == df['PM2.5'].max()]
max_pm10 = df[df['PM10'] == df['PM10'].max()]
max_so2 = df[df['SO2'] == df['SO2'].max()]
max_no2 = df[df['NO2'] == df['NO2'].max()]
max_co = df[df['CO'] == df['CO'].max()]
max_o3 = df[df['O3'] == df['O3'].max()]

# Print title
st.title('Simple Dashboard of AQI of Shunyi Area')

# Print date and time when each pollutant reaches its highest value
st.subheader("Date and time when each pollutant reaches its highest value:")
st.write("PM2.5:", max_pm25[['year', 'month', 'day', 'hour']])
st.write("PM10:", max_pm10[['year', 'month', 'day', 'hour']])
st.write("SO2:", max_so2[['year', 'month', 'day', 'hour']])
st.write("NO2:", max_no2[['year', 'month', 'day', 'hour']])
st.write("CO:", max_co[['year', 'month', 'day', 'hour']])
st.write("O3:", max_o3[['year', 'month', 'day', 'hour']])

# Calculate minimum values for each pollutant
min_pm25 = df[df['PM2.5'] == df['PM2.5'].min()]
min_pm10 = df[df['PM10'] == df['PM10'].min()]
min_so2 = df[df['SO2'] == df['SO2'].min()]
min_no2 = df[df['NO2'] == df['NO2'].min()]
min_co = df[df['CO'] == df['CO'].min()]
min_o3 = df[df['O3'] == df['O3'].min()]

# Print date and time when each pollutant reaches its lowest value
st.subheader("Date and time when each pollutant reaches its lowest value:")
st.write("PM2.5:", min_pm25[['year', 'month', 'day', 'hour']])
st.write("PM10:", min_pm10[['year', 'month', 'day', 'hour']])
st.write("SO2:", min_so2[['year', 'month', 'day', 'hour']])
st.write("NO2:", min_no2[['year', 'month', 'day', 'hour']])
st.write("CO:", min_co[['year', 'month', 'day', 'hour']])
st.write("O3:", min_o3[['year', 'month', 'day', 'hour']])

# Calculate mean and median concentrations of pollutants
pollutant_mean = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()
pollutant_median = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].median()

# Print mean and median concentrations of pollutants
st.subheader("Mean concentrations of pollutants:")
st.write(pollutant_mean)
st.subheader("Median concentrations of pollutants:")
st.write(pollutant_median)

# Define a function to calculate AQI
def calculate_aqi(pm25, pm10, so2, no2, co, o3):
    aqi = max(pm25, pm10, so2, no2, co, o3)
    return aqi

# Calculate AQI for each day
df['AQI'] = df.apply(lambda row: calculate_aqi(row['PM2.5'], row['PM10'], row['SO2'], row['NO2'], row['CO'], row['O3']), axis=1)

# Find the day with the highest AQI
day_max_aqi = df.loc[df['AQI'].idxmax()]

# Print the day with the highest AQI
st.subheader("The day with the highest AQI in Shunyi:")
st.write(f"- Date: {day_max_aqi['year']}/{day_max_aqi['month']}/{day_max_aqi['day']}")
st.write(f"- AQI: {day_max_aqi['AQI']}")

# Bar chart for showing the mean concentrations of pollutants
st.subheader("Mean Concentrations of Pollutants")
plt.figure(figsize=(10, 6))
pollutant_mean.plot(kind='bar', color='red')
plt.title("Mean Concentrations of Pollutants", loc="center", fontsize=15)
plt.xlabel('Pollutant')
plt.ylabel('Concentration (µg/m³ or ppm)')
plt.xticks(rotation=0)
st.pyplot(plt.gcf())

# Create a heatmap showing the correlation between weather variables and pollutant concentrations
st.subheader("Correlation between Weather Variables and Pollutant Concentrations")
weather_variables = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
selected_columns = weather_variables + pollutants
correlation_matrix = df[selected_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title('Correlation between Weather Variables and Pollutant Concentrations')
plt.xlabel('Pollutants')
plt.ylabel('Weather Variables')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
st.pyplot()
