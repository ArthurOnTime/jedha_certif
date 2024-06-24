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

    def __init__(self, hotels_source= None):
        # Read the hotels_sources file to init the Scraper
        with open(hotels_source, "r") as file:
            file = json.load(file)
            list_hotels = [element for element in file]
            list_url = [element["url"] for element in file]
        
        # Init Scraper variables
        self.list_hotels = list_hotels
        self.list_url = list_url
        self.counter = 0
        self.start_urls = [self.list_url[self.counter]]

    # Url to start your spider from -> TRY TO REMOVE
    #start_urls = [
     #   "https://www.booking.com/searchresults.fr.html?ss=Paris&checkin=2024-03-02&checkout=2024-03-05&group_adults=2&no_rooms=1&group_children=0"
    #]

    # Callback function that will be called when starting your spider
    def parse(self, response):

        yield {
            'city' : self.list_hotels[self.counter]['city'],
            'name' : self.list_hotels[self.counter]['name'],
            'url' : self.list_hotels[self.counter]['url'],
            'score': self.list_hotels[self.counter]['score'],
            'address': response.css('.hp_address_subtitle::text').get(),
            'desc' : response.css('p[data-testid="property-description"]::text').get(),
            #'desc2' : response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/p/text()').get(),
            }
        
        # Visit the hotel page
        if self.counter < len(self.list_url):
            self.counter += 1
            yield response.follow(self.list_url[self.counter], callback=self.parse)
         

# Name of the file where the results will be saved
filename = "hotels_details.json"

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



# Start the crawling using the spider you defined above
process.crawl(HotelSpider, hotels_source='src/hotels.json')
process.start()