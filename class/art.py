from collection import MYDB
import vercel_blob, vercel_blob.blob_store as vb_store
from datetime import datetime
from bson.objectid import ObjectId
from typing import Any
from pprint import pprint

class Art:
    _DBCOLLECTION = MYDB["arts"]

    def __init__(self, title: str, desc: str, url: str, price: int, *, artistID: ObjectId|None = None, country: str|None = None, tags: set[str] = set(), creationDate: datetime = datetime.now()) -> None:
        self.title: str = title
        self.desc: str = desc
        self.url: str = url
        self.price: int = price
        self.artistID: ObjectId|None = artistID
        self.tags: set[str] = tags
        self.creationDate: datetime = creationDate
        self.country: str|None = country

        existingData = self._findItem()
        if existingData is None:
            self._id = self._insertItem()
        else:
            self._id = existingData.get("_id")

    @staticmethod
    def fromDict(data: dict) -> Art:
        return Art(**data)

    @staticmethod
    def findArts(artistID: ObjectId) -> dict[str, Any]|None:
        userdata = Art._DBCOLLECTION.find_one({"artistID": artistID})
        return userdata

    def _insertItem(self) -> ObjectId|None:
        """Insert the art into the database. Please don't use this function during development."""
        idNum = self._DBCOLLECTION.insert_one(self.__dict__).inserted_id
        return idNum
        
    def _findItem(self) -> dict[str, Any] | None:
        return Art._DBCOLLECTION.find_one(self.__dict__)\
    
    def update(self) -> None:
        """Reflect the user's updated attributes into the database."""
        self._DBCOLLECTION.find_one_and_update({"_id": self._id}, {"$set": self.__dict__})
    
    def deleteItem(self, artistID) -> bool:
        """
        Delete the user from the database. Provide username and passHash to safely delete.
        
        :param self: The user that is going to be deleted from the database.
        :param username: A unique username. It does not start with @ symbol. Case insensitive (it is always in lowercase)
        :type username: str
        :param passHash: A hashed password.
        :param str: Description
        :return: 
        :rtype: bool
        """
        if artistID == self.artistID:
            self._DBCOLLECTION.delete_one({"_id": self._id})
            return True
        else:
            return False

def uploadArt():
    pass
       
if __name__ == "__main__":
    pass