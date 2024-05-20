import scrapy
import json
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        # Extract links to each author's page
        author_links = response.css('.author + a::attr(href)').getall()
        for author_link in author_links:
            yield scrapy.Request(url=response.urljoin(author_link), callback=self.parse_author)

    def parse_author(self, response):
        # Extract author details
        fullname = response.css('.author-title::text').get()
        born_date = response.xpath("//span[@class='author-born-date']/text()").get()
        born_location = response.xpath("//span[@class='author-born-location']/text()").get()
        description = response.css('.author-description::text').get()

        yield {
            "fullname": fullname.strip() if fullname else None,
            "born_date": born_date.strip() if born_date else None,
            "born_location": born_location.strip() if born_location else None,
            "description": description.strip() if description else None
        }

# Run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()

# Read the JSON output and rewrite it in a human-readable format
with open("authors.json", 'r', encoding="utf-8") as f:
    data = json.load(f)

with open("authors.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
