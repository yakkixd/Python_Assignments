import pandas as pd

df = pd.read_csv('weather_dataset.csv')
print(df.head())

import numpy as np
import pandas as pd

weather = pd.read_csv('weather_dataset.csv')

mean_temp = np.mean(weather['Temp'])
max_temp = np.max(weather['Temp'])
min_humidity = np.min(weather['Humidity'])
std_rainfall = np.std(weather['Rainfall'])

print('Mean Temp:', mean_temp)
print('Max Temp:', max_temp)
print('Min Humidity:', min_humidity)
print('Std Rainfall:', std_rainfall)

print(df.info())
print(df.describe())

df = df.dropna()
df['Date'] = pd.to_datetime(df['Date'])   # ← FIXED position

weather = df[['Date', 'Temp', 'Humidity', 'Rainfall']]

import matplotlib.pyplot as plt
import pandas as pd

weather = pd.read_csv('weather_dataset.csv')
weather['Date'] = pd.to_datetime(weather['Date'])  # ← FIXED position

plt.plot(weather['Date'], weather['Temp'])
plt.title('Daily Temperature Trend')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.savefig('temp_trend.png')
plt.show()
weather['Month'] = weather['Date'].dt.month   # ← works now!
monthly_rainfall = weather.groupby(weather['Month'])['Rainfall'].sum()
monthly_rainfall.plot(kind='bar')
plt.title('Monthly Rainfall')
plt.xlabel('Month')
plt.ylabel('Rainfall (mm)')
plt.savefig('monthly_rainfall.png')
plt.show()

# Scatter plot - Temp vs Humidity
plt.scatter(weather['Temp'], weather['Humidity'])
plt.title('Humidity vs Temperature')
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.savefig('humidity_temp_scatter.png')
plt.show()
