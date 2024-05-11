import scrapy
import json
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotes.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
            
# run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()

with open("quotes.json", 'r', encoding= "utf-8") as f:
    data = json.load(f)

with open("quotes.json", "w" ,encoding= "utf-8") as file:
    json.dump(data, file, indent = 4, ensure_ascii=False)


