import json
import requests
from bs4 import BeautifulSoup


def scrape_data(url, scrapped_data):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the article titles (assuming they are in <h2> tags)
        titles = soup.find_all('h1')
        data = []
        for i, title in enumerate(titles, start=1):
            x = f"{i}. {title.get_text().strip()}"
            data.append(x)


        # Save the data as a JSON file
        with open(scrapped_data, 'w') as json_file:
            json.dump(data, json_file)

        print(f"Data saved to {scrapped_data}")
    else:
        print(f"Failed to retrieve the content. Status code: {response.status_code}")