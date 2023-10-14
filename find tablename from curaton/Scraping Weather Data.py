import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of a weather forecast for a specific location
url = 'https://www.example-weather-site.com/location'

# Send an HTTP GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the elements containing weather data
    temperature = soup.find('span', class_='temperature').text.strip()
    condition = soup.find('div', class_='weather-condition').text.strip()

    # Create a list to store the data
    data = [['Location', 'Temperature', 'Condition'],
            ['Your Location Name', temperature, condition]]

    # Create a DataFrame using pandas
    df = pd.DataFrame(data, columns=['Location', 'Temperature', 'Condition'])

    # Save the DataFrame to an Excel file
    df.to_excel('weather_data.xlsx', index=False)

    print("Weather data has been scraped and saved to weather_data.xlsx.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
