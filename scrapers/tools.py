import os, pymongo
from dotenv import load_dotenv

class tools:

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