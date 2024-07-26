import streamlit as st
import pandas as pd
import requests


# Function to fetch weather data
def get_weather_data(city_name):
    api_key = '79e62f2d0518c73492fd68d8cde6ee68'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Streamlit app
st.title('Weather Forecast App')

# Input for city name
city = st.text_input('Enter city name:')

if city:
    data = get_weather_data(city)
    if data:
        if 'main' in data:
            st.success('Data fetched successfully!')
            st.write(f"City: {data['name']}, {data['sys']['country']}")
            st.write(f"Temperature: {data['main']['temp']}°C")
            
            # Print the data for debugging
            st.write(data)

            # Line chart for temperature
            temp_data = pd.DataFrame({
                'Temperature': [data['main']['temp']],
                'Feels Like': [data['main']['feels_like']],
                'Min Temp': [data['main']['temp_min']],
                'Max Temp': [data['main']['temp_max']]
            }, index=[city])
            st.line_chart(temp_data)

            # Bar chart for humidity
            humidity_data = pd.DataFrame({'Humidity': [data['main']['humidity']]}, index=[city])
            st.bar_chart(humidity_data)

            # Map for location
            map_data = pd.DataFrame({'lat': [data['coord']['lat']], 'lon': [data['coord']['lon']]})
            st.map(map_data)

            # Show raw data
            if st.checkbox('Show raw data'):
                st.write(data)

            # Additional widgets relevant to weather data
            st.radio('Select weather condition:', [data['weather'][0]['main']])
            st.selectbox('Select temperature range:', [f"{data['main']['temp_min']}°C - {data['main']['temp_max']}°C"])
            st.multiselect('Select weather details:',
                           ['Temperature', 'Feels Like', 'Humidity', 'Wind Speed', 'Pressure', 'Visibility',
                            'Cloudiness'])

            # Date and time input
            st.date_input('Select date:', pd.to_datetime(data['dt'], unit='s'))
            st.time_input('Select time:', pd.to_datetime(data['dt'], unit='s').time())
            st.file_uploader('Upload weather data file:')
            st.color_picker('Pick a color for weather visualization:')
        else:
            st.error('Unexpected data format received from the API.')
    else:
        st.error('City not found or API request failed!')
else:
    st.info('Please enter a city name to get the weather forecast.')
