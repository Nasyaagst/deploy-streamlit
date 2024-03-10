import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import streamlit as st

df = pd.read_csv("https://raw.githubusercontent.com/Nasyaagst/Submission/main/all_data.csv")

# Print title
st.title('Simple Dashboard of AQI (Air Quality Index) of Shunyi Area')

# Add Name Widget
name = name.upper()
name = st.text_input(label='Your Name', value='', placeholder='First, please type your name here')

if name:
    st.write('Hello,', name + "!")
    st.write("AQI, standing for Air Quality Index, serves as a vital tool to assess the air we breathe. By analyzing various pollutants such as particulate matter (PM2.5 and PM10), ozone (O3), sulfur dioxide (SO2), nitrogen dioxide (NO2), and carbon monoxide (CO), it provides insights into potential health risks associated with air pollution, guiding individuals to take necessary precautions.")
    st.write("Shunyi, a district located in the northeastern part of Beijing, China, boasts a suburban environment characterized by its tranquil surroundings and lush greenery. However, being part of the Beijing Municipality, Shunyi is also affected by air pollution, which can vary depending on factors such as weather conditions, industrial activity, and vehicular emissions.")
    st.write("This dashboard provides data ranging from **March 1st 2013 until February 28th 2017** 24 hours non-stop about Air Quality in Shunyi, allowing residents and visitors to monitor air quality levels closely. By staying informed about AQI readings, you can take appropriate measures to protect your health, such as avoiding outdoor activities during periods of high pollution and using air purifiers indoors.")

else:
    st.write("To show description, please type your name first in the box above!")

col1 = st.columns(2)

def calculate_aqi(pm25, pm10, so2, no2, co, o3):
    aqi = max(pm25, pm10, so2, no2, co, o3)
    return aqi

# Calculate AQI for each day
df['AQI'] = df.apply(lambda row: calculate_aqi(row['PM2.5'], row['PM10'], row['SO2'], row['NO2'], row['CO'], row['O3']), axis=1)

# Find the day with the highest AQI
day_max_aqi = df.loc[df['AQI'].idxmax()]

# Print the day with the highest AQI
st.subheader("When was Shunyi's AQI at its peak? How high was it?")
col1, col2 = st.columns(2)

with col1:
    st.metric("**Date**", f"{day_max_aqi['year']}/{day_max_aqi['month']}/{day_max_aqi['day']}")
    
with col2:
    st.metric("**AQI**", value=day_max_aqi['AQI'])

# Calculate maximum values for each pollutant
max_pm25 = df[df['PM2.5'] == df['PM2.5'].max()]
max_pm10 = df[df['PM10'] == df['PM10'].max()]
max_so2 = df[df['SO2'] == df['SO2'].max()]
max_no2 = df[df['NO2'] == df['NO2'].max()]
max_co = df[df['CO'] == df['CO'].max()]
max_o3 = df[df['O3'] == df['O3'].max()]

# Print date and time when each pollutant reaches its highest value
st.write("")
st.subheader("Seeking more details? Here is the list on the exact date and time for each pollutant's reaches its highest value!")

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
st.subheader("Now, let's turn our attention to when each pollutant reaches its lowest value!")
st.write("PM2.5:", min_pm25[['year', 'month', 'day', 'hour']])
st.write("PM10:", min_pm10[['year', 'month', 'day', 'hour']])
st.write("SO2:", min_so2[['year', 'month', 'day', 'hour']])
st.write("NO2:", min_no2[['year', 'month', 'day', 'hour']])
st.write("CO:", min_co[['year', 'month', 'day', 'hour']])
st.write("O3:", min_o3[['year', 'month', 'day', 'hour']])

# Calculate mean and median concentrations of pollutants
pollutant_mean = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

# Show bar chart for showing the mean concentrations of pollutants
st.subheader("Mean Concentrations of Each Pollutants")
plt.figure(figsize=(10, 6))
ax = pollutant_mean.plot(kind='bar', color='red')
plt.title("Mean Concentrations of Pollutants", loc="center", fontsize=15)
plt.xlabel('Pollutant')
plt.ylabel('Concentration (µg/m³ or ppm)')
plt.xticks(rotation=0)

# Adding value labels on top of each bar with space
for i, v in enumerate(pollutant_mean):
    ax.annotate(str(round(v, 2)), xy=(i, v), xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

st.pyplot(plt.gcf())

# Create a heatmap showing the correlation between weather variables and pollutant concentrations
st.subheader("Correlation between Weather Variables and Pollutant Concentrations")
weather_variables = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
selected_columns = weather_variables + pollutants
correlation_matrix = df[selected_columns].corr()

fig, ax = plt.subplots(figsize=(10, 8))  # Create a new figure with the desired size
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, ax=ax)
plt.title('Correlation between Weather Variables and Pollutant Concentrations')
plt.xlabel('Pollutants')
plt.ylabel('Weather Variables')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
st.pyplot(fig)  # Display the figure using st.pyplot()
