if __name__ == "__main__":
    from collection import MYDB
    from user import User
else:
    from entities.collection import MYDB
    from entities.user import User
import vercel_blob, vercel_blob.blob_store as vb_store
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from typing import Any, Generator
from pprint import pprint
from io import BytesIO

class Art:
    _DBCOLLECTION = MYDB["arts"]

    def __init__(self, title: str, desc: str, url: str, price: int, *, artistID: ObjectId|None = None, country: str|None = None, tags: list[str]|None = None, creationDate: datetime = datetime.now(), _id: ObjectId|None = None) -> None:
        self.title: str = title
        self.desc: str = desc
        self.url: str = url
        self.price: int = price
        self.artistID: ObjectId|None = artistID
        self.tags: list[str] = [] if tags is None else tags
        self.creationDate: datetime = creationDate
        self.country: str|None = country

        existingData = self._findItem()
        if existingData is None:
            self._id = self._insertItem()
        else:
            self._id = existingData.get("_id")

    def getPrice(self) -> str:
        return str(self.price // 100) + "." + str(self.price % 100).rjust(2, "0")

    def getAge(self) -> timedelta:
        return datetime.now() - self.creationDate

    @staticmethod
    def fromDict(data: dict):
        return Art(**data)

    @staticmethod
    def findArtsFromArtist(artistID: ObjectId): #-> list[dict[str, Any]]|None:
        artsdata = Art._DBCOLLECTION.find({"artistID": artistID})
        for artdata in artsdata:
            yield Art.fromDict(artdata)
    
    @staticmethod
    def findArt(artID: ObjectId): # -> Art|None:
        artdata = Art._DBCOLLECTION.find_one({"_id": artID})
        if not artdata:
            return
        return Art.fromDict(artdata)

    @staticmethod
    def getAllArts():
        artdata = Art._DBCOLLECTION.find()
        for artdatum in artdata:
            yield Art.fromDict(artdatum)


    def _insertItem(self) -> ObjectId|None:
        """Insert the art into the database. Please don't use this function during development."""
        idNum = self._DBCOLLECTION.insert_one(self.__dict__).inserted_id
        return idNum
        
    def _findItem(self) -> dict[str, Any] | None:
        return Art._DBCOLLECTION.find_one({k: v for k, v in self.__dict__.items() if k != "creationDate"})\
    
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

def uploadArt(artist: User, imageBuffer: BytesIO, extension: str) -> dict[str, Any]:
    """
    Upload the artwork into the blob storage

    :param artist: The user instance that creates the artwork.
    :type artist: User
    :param imageBuffer: The artwork file buffer that the artist created.
    :type imageBuffer: BytesIO
    :param extension: The artwork file extension.
    :type extension: str
    :return: The vercel_blob upload response, containing keys: 'downloadUrl', 'pathname', 'url'.
    :rtype: dict[str, Any]
    """
    filename:str = f"A_{artist.username}{int(datetime.now().timestamp())}"
    resp = vercel_blob.put(f'{filename}.{extension}', imageBuffer.read(), multipart=True, verbose=True)
    return resp
       
if __name__ == "__main__":
    for doc in Art._DBCOLLECTION.find():
        pprint(doc)
    # username: str = input("Username: @")
    # myUser = User.findItem(username)
    # if not myUser: quit()
    # print(f"@{myUser.username} exists!")
    # filename = uploadArt(myUser)
    # print(filename)


    # myArt = Art(
    #     "Happy Strike", 
    #     "A happy fox!",
    #     "https://vintageharmonies.neocities.org/sprites/sprite%205.png",
    #     1000, artistID = ObjectId("697dd5e443e3a7ac598cf3c7"),
    #     country = "Indonesia",
    #     tags = ["fox", "digital", "sticker"])
    
    # print(myArt._id)
    # print(myArt.__dict__)

    # arts = Art.findArts(ObjectId("697dd5e443e3a7ac598cf3c7"))
    # for art in arts:
    #     pprint(art)

    # myArt = Art.findArt(ObjectId("697e182922884bbed78df3f4"))
    # pprint(myArt.__dict__)
    # if not myArt: quit()
    # myArt.title = "Strike Full of Joy"
    # pprint(myArt.__dict__)
    # myArt.update()

    # myArt = Art.findArt(ObjectId("697e182922884bbed78df3f4"))
    # if myArt:
    #     print(myArt.deleteItem(ObjectId("697dd5e443e3a7ac598cf3c7")))