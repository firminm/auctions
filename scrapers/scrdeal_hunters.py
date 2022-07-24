import requests, os, pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from time import sleep
from datetime import datetime
from dotenv import load_dotenv

"""
    ---------------------------------------------------
    --             WARNING - DEPRECATED              --
    --PLEASE USE scpdeal_hunters.py AS CODE REFERENCE--
    ---------------------------------------------------
"""

BASE = 'https://dealhunterauction.hibid.com/'

def scrape_auction_houses():
    '''
        Gets the list of auction houses from the main page
        When a new auction house is found, calls scrape_venue() for that auction
    '''
    r = requests.get(BASE)
    soup = BeautifulSoup(r.content, features='html.parser')
    rows = soup.find('body', class_='AUCTIONS_HOME_INDEX').find('table').find('tbody').find_all('tr', class_='auction-list-details-panel')

    venues = [] 
    for auction_block in rows:
        venue = {}  # Holds the data about the estate sale venue

        # Scrape header of row item
        link = auction_block.find('div', class_='panel-heading').find('a')
        venue['title'] = link.get_text(strip=True)
        venue['link'] = BASE + link.get('href')

        #Scrape body of row item
        body = auction_block.find('div', class_='panel-body')
        venue['hasAddress'] = False    # Address only provided to winners - hard coding this as it's standard for this site
        venue['location'] = body.find('div', class_='lot-auction-info-location text-nowrap').find('a').get_text(strip=True).replace('\xa0', ' ')
        venue['dates'] = body.find('h5').get_text(strip=True)[7:].strip()

        venue['details'] = body.find('div', class_='auction-details-description-container text-pre-line collapse').get_text(strip=True)

        venues.append(venue)
    
    addVenuesToDb(venues)
    return venues
    


def scrape_lot(url, page=1, query=None):
    '''
        Gets data on every item in the lot
        
        Called from scrape_auction_houses when a new lot is added to their website
        Called periodically from server to have updated bid prices and listings
    '''
    # ipp=10 flag to show all results on one page (instead of having to load multiple pages... this is site specific)
    print(page)
    lot_url = url+f'?cpage={page}'
    if query:
        # query capability here just in case it's needed down the line
        lot_url = lot_url + f'&q={query}&m=1&ipp=100'
    else:
        lot_url = lot_url + '&ipp=100'
    
    # Web driver required to load dynamic page
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service("c:\webdrivers\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(lot_url)
    except:
        print('Load error, retrying')
        scrape_lot(url, page, query=query)
        return
    sleep(8)    # sleep to ensure page is loaded

    r = driver.page_source

    # r = requests.get(lot_url)
    now = datetime.now()    # call immediately after requests is return to minimize lag
    soup = BeautifulSoup(r, features='html.parser')
    row = soup.find('body', class_='CATALOG_DETAILS_INDEX').find('div', class_='container')
    row= row.find('div', class_='col-xs-12 p-x')
    # rows = rows.find('tbody')
    # rows = rows.find_all('tr')
    rows = row.find_all('div', class_='lot-tile col-md-3 col-lg-2 p-x-xs px-md-1')

    listings = [] 
    for block in rows:
        # log_block(block, 2)

        item = {}   # Holds the data for each listed item

        title_data = block.find('a', class_='lot-number-lead lot-link remove-underline lot-title-ellipsis lot-preview-link')
        item['link'] = BASE + title_data.get('href')

        # Title is formatted like: Lot 300 | Name of item
        item['lot'], item['title'] = title_data.get_text().split(' | ')


        item['bids'] = block.find('a', class_='lot-bid-history btn btn-link p-a-0').get_text()
        item['timeLeftOnScrape'] = block.find('div', class_='lot-time-label lot-time-label-lg label inline-block label-info').find('span').get_text()
        item['timeofScrape'] = now

        item['highBid'] = block.find('span', class_='lot-high-bid').get_text()

        listings.append(item)
        # break
    
    addListingsToDb(listings)
    
    if(row.find('div', class_='dataTables_paginate paging_simple_numbers').find('li', {'class': 'paginate_button next', 'id': 'lot-list_next'})):
        scrape_lot(url, page+1, query=query)
    else:
        print('next not found')


def log_block(block, num=0):
    '''
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

def main():
    venues = scrape_auction_houses()
    load_dotenv()
    client_key = os.getenv('client')
    client = pymongo.MongoClient(client_key)
    db = client.estateData
    listing_coll = db['listings']

    listing_coll.drop() # TODO: delete 

    for i, venue in enumerate(venues):
        scrape_lot(venue['link'])


if __name__ == '__main__':
    main()
