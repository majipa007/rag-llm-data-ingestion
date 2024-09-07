import scrapy

class CollegeSpider(scrapy.Spider):
    name = "college"
    
    # Start with the URL passed during runtime
    def start_requests(self):
        url = getattr(self, 'url', None)
        if url is not None:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract all the text from the page
        page_text = response.xpath("//body//text()").getall()
        page_text = [text.strip() for text in page_text if text.strip()]
        
        # Yield the results
        yield {
            'url': response.url,
            'text': page_text,
        }

        # Follow links to other pages
        links = response.xpath("//a/@href").extract()
        for link in links:
            if link and not link.startswith('http'):
                link = response.urljoin(link)
            if link.startswith(response.url):
                yield scrapy.Request(link, callback=self.parse)
