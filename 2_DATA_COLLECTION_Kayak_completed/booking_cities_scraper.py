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
import csv

class BookingSpider(scrapy.Spider):

    # Name of your spider
    name = "BookingSpider"

    def __init__(self, cities_source= None):
        # Read the cities_sources file to init the Scraper
        with open(cities_source, "r") as file:
            reader = csv.reader(file)
            next(reader)
            list_cities = []
            list_url = []
            for row in reader:
                city = row[12].replace(' ','%20')
                list_cities.append(city)
                list_url.append("https://www.booking.com/searchresults.fr.html?ss={}&checkin=2024-04-02&checkout=2024-04-03&group_adults=2&no_rooms=1&group_children=0".format(city))
        # Init Scraper variables
        self.list_cities = list_cities
        self.list_url = list_url
        self.counter = 0 
        self.start_urls = [self.list_url[self.counter]]


    # Callback function that will be called when starting your spider
    def parse(self, response):
        # List property-card <div> from search results
        hotels = response.css('div[data-testid="property-card"]')
        # Extract relevant data from each property-card <div>
        for hotel in hotels:
            # Skip property-card if Advertising
            if not hotel.xpath('div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/span/span/span/text()').get() == "Publicité":
                 
                # Return the hotel's data from the property-card <div>
                yield {
                    'city': self.list_cities[self.counter],
                    'name': hotel.xpath('div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/h3/a/div[1]/text()').get(),
                    'url': hotel.xpath('div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/h3/a').attrib["href"],
                    'score': hotel.xpath('div[1]/div[2]/div/div[1]/div[2]/div/div/a/span/div/div[1]/text()').get(),
                    }
        
        # Search the next city in the cities_source list
        if self.counter < len(self.list_url):
            self.counter += 1
            yield response.follow(self.list_url[self.counter], callback=self.parse)

# Name of the file where the results will be saved
filename = "hotels.json"

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
process.crawl(BookingSpider, cities_source='src/cities.csv')
process.start()