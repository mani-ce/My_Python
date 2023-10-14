import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the IMDb Top 250 movies page
url = 'https://www.imdb.com/chart/top'

# Send an HTTP GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the movie list
    table = soup.find('table', class_='chart')

    # Create a list to store the data
    data = []

    # Iterate through the rows of the table and extract data
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 5:
            title = cells[1].text.strip()
            rating = cells[2].text.strip()
            data.append([title, rating])

    # Create a DataFrame using pandas
    df = pd.DataFrame(data, columns=['Title', 'Rating'])

    # Save the DataFrame to an Excel file
    df.to_excel('top_movies.xlsx', index=False)

    print("Top movies data has been scraped and saved to top_movies.xlsx.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
