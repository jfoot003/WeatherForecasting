import streamlit as st
import pandas as pd
import requests


# Function to fetch weather data
def get_weather_data(city_name):
    api_key = 'YOUR_API_KEY'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()


# Streamlit app
st.title('Weather Forecast App')

# Input for city name
city = st.text_input('Enter city name:')

if city:
    data = get_weather_data(city)
    if data:
        st.success('Data fetched successfully!')
        st.write(f"Temperature: {data['main']['temp']}°C")
        st.write(f"Weather: {data['weather'][0]['description']}")
        st.write(f"Humidity: {data['main']['humidity']}%")
        st.write(f"Wind Speed: {data['wind']['speed']} m/s")

        # Line chart for temperature
        temp_data = pd.DataFrame({'Temperature': [data['main']['temp']]}, index=[city])
        st.line_chart(temp_data)

        # Area chart for temperature
        st.area_chart(temp_data)

        # Bar chart for temperature
        st.bar_chart(temp_data)

        # Map for location
        map_data = pd.DataFrame({'lat': [data['coord']['lat']], 'lon': [data['coord']['lon']]})
        st.map(map_data)

        # Show raw data
        if st.checkbox('Show raw data'):
            st.write(data)

        # Interactive table
        st.dataframe(temp_data)

        # Additional widgets
        st.radio('Choose an option:', ['Option 1', 'Option 2', 'Option 3'])
        st.selectbox('Select an option:', ['Option A', 'Option B', 'Option C'])
        st.multiselect('Select multiple options:', ['Option X', 'Option Y', 'Option Z'])
        st.slider('Select a range of values:', 0, 100, (25, 75))
        st.select_slider('Select a value:', options=['Low', 'Medium', 'High'])
        st.text_area('Enter some text:')
        st.date_input('Select a date:')
        st.time_input('Select a time:')
        st.file_uploader('Upload a file:')
        st.color_picker('Pick a color:')
    else:
        st.error('City not found!')
else:
    st.info('Please enter a city name to get the weather forecast.')
