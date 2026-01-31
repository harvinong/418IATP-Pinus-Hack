from collection import MYDB
from datetime import datetime
from bson.objectid import ObjectId
from typing import Any
from pprint import pprint

class User:
    _DBCOLLECTION = MYDB["users"]

    def __init__(self, username: str, passHash: str, fullName: str, surName: str|None = None, creationDate: datetime = datetime.now(), country: str|None = None, website: str|None = None, _id: ObjectId|None = None) -> None:
        self.username: str = username
        self.passHash: str = passHash
        self.fullName: str = fullName
        self.surName: str|None = surName
        self.creationDate: datetime = creationDate
        self.country: str|None = country
        self.website: str|None = website

        existingData = self.findItem(self.username)
        if existingData is None:
            self._id = self._insertItem()
        else:
            self._id = existingData.get("_id")

    @staticmethod
    def fromDict(data: dict) -> User:
        return User(**data)

    @staticmethod
    def findItem(username: str) -> dict[str, Any]|None:
        userdata = User._DBCOLLECTION.find_one({"username": username})
        return userdata
    
    def _insertItem(self) -> ObjectId|None:
        existingData = self.findItem(self.username)
        if existingData is None:
            idNum = self._DBCOLLECTION.insert_one(self.__dict__).inserted_id
            return idNum
    
    def update(self) -> None:
        self._DBCOLLECTION.find_one_and_update({"_id": self._id}, {"$set": self.__dict__})
    
    def deleteItem(self) -> None:
        self._DBCOLLECTION.delete_one({"_id": self._id})

if __name__ == "__main__":
    # myUser = User("@jeffbezo", "12345678", "Jeffrey", "Bezo", country = "Amazon")
    # pprint(User.findItem("@whansel"))
    # pprint(User.findItem("@Mark"))
    for doc in User._DBCOLLECTION.find():
        pprint(doc)