import requests
from bs4 import BeautifulSoup

def extract_medium_text(url):
    # Send a GET request to the Medium article URL
    response = requests.get(url)
    
    # Parse the content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main content of the Medium article
    # Medium articles typically use the 'section' tag for the main article body.
    article_section = soup.find('article')
    
    if article_section:
        # Extract all the text within paragraphs, headers, and other common text tags
        paragraphs = article_section.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'])
        article_text = "\n\n".join([p.get_text() for p in paragraphs])
        
        return article_text
    else:
        return "No article content found"

# Example usage
url = input("enter the url:\n")  # Replace this with the actual Medium article URL
article_text = extract_medium_text(url)
print(article_text)


