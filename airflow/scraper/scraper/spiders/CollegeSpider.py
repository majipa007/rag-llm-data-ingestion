import scrapy
import json
import numpy as np
from pathlib import Path

class CollegeSpider(scrapy.Spider):
    name = "college"
    
    # Start with the URL passed during runtime
    def start_requests(self):
        url = getattr(self, 'url', None)
        if url is not None:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # For demonstration purposes, let's assume we are generating random vectors for each page
        page_text = response.xpath("//body//text()").getall()
        page_text = [text.strip() for text in page_text if text.strip()]

        # Create random vector representation (example)
        random_vector = np.random.rand(128).tolist()  # Assume 128-dimension vector for simplicity

        # Example entry to save (id and vector)
        entry = {
            'id': response.url,  # Use URL as unique identifier
            'vector': random_vector  # Use random vectors for demo
        }

        # Save the scraped data to a JSON file in the designated folder
        scraped_data_folder = "scraped_data"  # Make sure this exists or create it
        Path(scraped_data_folder).mkdir(parents=True, exist_ok=True)

        file_path = Path(scraped_data_folder) / f"{response.url.replace('/', '_')}.json"
        
        with open(file_path, 'w') as f:
            json.dump([entry], f)

        print(f"Saved vector data for {response.url} to {file_path}")

        # Follow links to other pages (for a recursive scrape)
        links = response.xpath("//a/@href").extract()
        for link in links:
            if link and not link.startswith('http'):
                link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse)
