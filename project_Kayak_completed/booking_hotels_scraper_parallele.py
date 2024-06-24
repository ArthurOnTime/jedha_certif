# Import os => Library used to easily manipulate operating systems
## More info => https://docs.python.org/3/library/os.html
import os 

# Import logging => Library used for logs manipulation 
## More info => https://docs.python.org/3/library/logging.html
import logging

# Import scrapy 
import scrapy
from scrapy.crawler import CrawlerProcess

# Import cities.csv file to create the start_urls list
import json

class HotelSpider(scrapy.Spider):

    # Name of your spider
    name = "HotelSpider"

    def __init__(self, hotel= None): 
        # Init Scraper variables
        self.hotel = hotel
        self.start_urls = [hotel['url']]

    # Callback function that will be called when starting your spider
    def parse(self, response):

        yield {
            'city' : self.hotel['city'],
            'name' : self.hotel['name'],
            'url' : self.hotel['url'],
            'score': self.hotel['score'],
            'address': response.css('.hp_address_subtitle::text').get(),
            'desc' : response.css('p[data-testid="property-description"]::text').get(),
            }

# Name of the file where the results will be saved
filename = "hotels_details_parallele.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src/' + filename: {"format": "json"},
    }
})

# Read the hotels_sources file to init the Scraper
with open('src/hotels.json', "r") as file:
    file = json.load(file)
    list_hotels = [element for element in file]
# Create // scrappers
for i, hotel in enumerate(file):
    if i > 300:
        process.crawl(HotelSpider, hotel=hotel)

# Start the crawling using the spider you defined above
process.start()