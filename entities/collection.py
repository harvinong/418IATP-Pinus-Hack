# Reference: https://www.w3schools.com/python/python_mongodb_getstarted.asp
import pymongo, os
from pprint import pprint
import vercel_blob, vercel_blob.blob_store as vb_store

MONGODB_URI: str = os.environ.get("MONGODB_URI", "")
if MONGODB_URI == "":
    raise ValueError("MONGODB_URI is not assigned")
CLIENT = pymongo.MongoClient(MONGODB_URI)
MYDB = CLIENT["JalaArtMarket"]

# Reference: https://medium.com/@suryasekhar/how-to-use-vercel-blob-storage-with-python-94785d3ea0b3
import vercel_blob, vercel_blob.blob_store as vb_store
BLOB_READ_WRITE_TOKEN: str = os.environ["BLOB_READ_WRITE_TOKEN"]
if BLOB_READ_WRITE_TOKEN == "":
    raise ValueError("BLOB_READ_WRITE_TOKEN is not assigned")

if __name__ == "__main__":
    print("Mongodb: " + MONGODB_URI[:16] + "...")
    print("Blob: " + BLOB_READ_WRITE_TOKEN[:16] + "...")
    print()
    print("MongoDB:")
    for collection in MYDB.list_collection_names():
        print(collection)
        collobject = MYDB[collection]
        for doc in collobject.find():
            pprint(doc)
    print()
    print("Blob:")
    pprint(vercel_blob.list())

    
