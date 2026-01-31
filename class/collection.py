# Reference: https://www.w3schools.com/python/python_mongodb_getstarted.asp
import pymongo, os
from pprint import pprint

MONGODB_URI: str = os.environ["MONGODB_URI"]
CLIENT = pymongo.MongoClient(MONGODB_URI)
MYDB = CLIENT["JalaArtMarket"]

if __name__ == "__main__":
    for collection in MYDB.list_collection_names():
        print(collection)
        collobject = MYDB[collection]
        for doc in collobject.find():
            pprint(doc)

    
