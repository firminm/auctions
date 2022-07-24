import os, pymongo
from abc import abstractclassmethod
from dotenv import load_dotenv

""" 
The following imports must exist within your subclass: 

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import datetime
from scrapers.scraper import Scraper
"""

class Scraper:
    """
        Overall outline for how scrapers should be created.
        
        In creating your subclass you MUST write your own "scrape" method

        All other methods are usable by doing:
          > scr = Scraper(<your url>)   # Creating a scraper, note you will have to make your own subclass
          > scr.log_block               # Using a method
    """
    def __init__(self, url, name="NoName"):
        self.url = url
        self.name = name

    def log_block(self, block, num=0):
        '''
            DEBUG TOOL -- Use to find out what you're looking at
            Creates a html file that stores the HTML tree, use this when you want to ctrl+F for a tag or figure out where something is on a page
            @param block: soup descendant (basically something from a soup.find()) to read the page source.
            @param num: suffix added to file to differentiate between calls
        '''
        with open(f'demo{num}.html', 'w') as f:
            f.write(block.prettify())

    def addListingsToDb(listings):
        '''
            Takes a list of documents to add to the database as input
        '''
        load_dotenv()
        client_key = os.getenv('client')
        client = pymongo.MongoClient(client_key)
        db = client.estateData
        listing_coll = db['listings']

        listing_coll.insert_many(listings)

    def addVenuesToDb(venues):
        load_dotenv()
        client_key = os.getenv('client')
        client = pymongo.MongoClient(client_key)
        db = client.estateData
        venue_coll = db['venues']

        venue_coll.drop()     # Testing tool TODO: delete
        venue_coll.insert_many(venues)

    @abstractclassmethod
    def scrape(self):
        '''
            Must be implemented in the subclass
        '''
        print("WARNING - THIS METHOD HAS NOT BEEN IMPLEMENTED")
        pass