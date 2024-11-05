
import requests
from bs4 import BeautifulSoup
import os

def extract_medium_text(url, save_path):
    # Send a GET request to the Medium article URL
    response = requests.get(url)
    
    # Parse the content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main content of the Medium article
    article_section = soup.find('article')
    
    if article_section:
        # Extract all the text within paragraphs, headers, and other common text tags
        paragraphs = article_section.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'])
        article_text = "\n\n".join([p.get_text() for p in paragraphs])
        
        # Save the article text to the specified path
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(article_text)
        return f"Content saved to {save_path}"
    else:
        return "No article content found"

# Example usage
#url = "https://medium.com/@sulavstha007/quantizing-yolo-v8-models-34c39a2c10e2"  # Replace with the actual article URL
#save_path = "../Scrapped_data/data.txt"  # Define your save path
#result = extract_medium_text(url, save_path)
#print(result)
