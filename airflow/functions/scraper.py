import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time

def scrape_data(url, output_file):
    visited = set()
    all_texts = []

    def scrape_page(url):
        if url in visited:
            return
        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        text_elements = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'div']
        text = ' '.join([element.get_text(strip=True) for tag in text_elements for element in soup.find_all(tag)])
        
        if text:
            all_texts.append({"url": url, "text": text})

        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                scrape_page(full_url)
            time.sleep(1)  # Add a delay to be polite

    scrape_page(url)

    # Save as JSON
    output_file.parent.mkdir(parents=True, exist_ok=True)  # Create folder if doesn't exist
    with open(output_file, 'w') as json_file:
        json.dump(all_texts, json_file, indent=4)
    print(f"Scraping completed and data saved to {output_file}")

