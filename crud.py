# Reference: https://www.w3schools.com/python/python_mongodb_getstarted.asp
import pymongo, os
from datetime import datetime
from pprint import pprint

MONGODB_URI: str = os.environ["MONGODB_URI"]
CLIENT = pymongo.MongoClient(MONGODB_URI)
MYDB = CLIENT["JalaArtMarket"]


class User:
    _DBCOLLECTION = MYDB["users"]

    def __init__(self, username: str, passHash: str, fullName: str, surName: str|None = None, creationDate: datetime = datetime.now(), country: str|None = None, website: str|None = None) -> None:
        self.username: str = username
        self.passHash: str = passHash
        self.fullName: str = fullName
        self.surName: str|None = surName
        self.creationDate: datetime = creationDate
        self.country: str|None = country
        self.website: str|None = website

    @staticmethod
    def getItem(username: str):
        return User._DBCOLLECTION.find_one({"username": username})
    
    def setItem(self) -> int:
        return self._DBCOLLECTION.insert_one(self.__dict__).inserted_id
    

if __name__ == "__main__":
    print(MYDB.list_collection_names())
    
    # userdata = [
    #     {"name": "Harvin", "age": 19, "species": "fox"},
    #     {"name": "Jack", "age": 20, "species": "alpha wolf/angel/demon"},
    #     {"name": "William", "age": 18, "species": "cat"},
    # ]

    # x = usersColl.insert_many(userdata)

    # print(x.inserted_ids)
    # print(mydb.list_collection_names())
    # userinstances = [
    #     User("@harvinong", "xxxxxx", "Harvin", country = "Indonesia", website = "vintageharmonies.neocities.org"),
    #     User("@jackchris", "xxxxxx", "Jack", country = "Indonesia"),
    #     User("@whansel", "xxxxxx", "William", country = "Indonesia")
    # ]

    # for inst in userinstances:
    #     pprint(User.getItem(inst.username))
    pprint(User.getItem("@harvinong"))