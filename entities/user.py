from entities.collection import MYDB
from datetime import datetime
from bson.objectid import ObjectId
from typing import Any, Self
from pprint import pprint

class User:
    _DBCOLLECTION = MYDB["users"]

    def __init__(self, username: str, passHash: str, fullName: str, surName: str|None = None, *, country: str|None = None, website: str|None = None, creationDate: datetime = datetime.now(), _id: ObjectId|None = None) -> None:
        """
        User is someone who uses the service. They can be a collector, an artist, or both.
        
        :param username: A unique username. It does not start with @ symbol. Case insensitive (it is always in lowercase)
        :type username: str
        :param passHash: A hashed password.
        :type passHash: str
        :param fullName: The full name of the user.
        :type fullName: str
        :param surName: The surname of the user.
        :type surName: str | None
        :param country: The country the user is based in.
        :type country: str | None
        :param website: The user's website's URL. Assign the full URL.
        :type website: str | None
        """
        self.username: str = username.lower()
        self.passHash: str = passHash
        self.fullName: str = fullName
        self.surName: str|None = surName
        self.creationDate: datetime = creationDate
        self.country: str|None = country
        self.website: str|None = website

        existingData = self._findItemData(self.username)
        if existingData is None:
            self._id = self._insertItem()
        else:
            self._id = existingData.get("_id")

    @staticmethod
    def fromDict(data: dict):
        """
        Instantiate User from a data dictionary. Best paired with User.findItem().
        
        :param data: The full dictionary data. Recommended to use the User.findItem() result.
        :type data: dict
        :return: The user object/instance.
        :rtype: User
        """
        return User(**data)

    @staticmethod
    def _findItemData(username: str) -> dict[str, Any]|None:
        """
        Find a user by their username.
        
        :param username: A unique username. It does not start with @ symbol. Case insensitive (it is always in lowercase)
        :type username: str
        :return: a data dictionary if the user is found. None otherwise.
        :rtype: dict[str, Any] | None
        """
        userdata = User._DBCOLLECTION.find_one({"username": username.lower()})
        return userdata
    
    @staticmethod
    def findItem(username: str): # -> User|None:
        userData = User._findItemData(username)
        if userData:
            return User.fromDict(userData)
        
    @staticmethod
    def findItemByID(userID: ObjectId): # -> User|None:
        userData = User._DBCOLLECTION.find_one({"_id": userID})
        if userData:
            return User.fromDict(userData)

    
    def _insertItem(self) -> ObjectId|None:
        """Insert the user into the database. Please don't use this function during development."""
        idNum = self._DBCOLLECTION.insert_one(self.__dict__).inserted_id
        return idNum
    
    def update(self) -> None:
        """Reflect the user's updated attributes into the database."""
        self._DBCOLLECTION.find_one_and_update({"_id": self._id}, {"$set": self.__dict__})
    
    def deleteItem(self, username: str, passHash, str) -> bool:
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
        if username.lower() == self.username and passHash == self.passHash:
            self._DBCOLLECTION.delete_one({"_id": self._id})
            return True
        else:
            return False
    
    def __repr__(self) -> str:
        return f"@{self.username} (id: {self._id.__str__()[-16:]})"

if __name__ == "__main__":
    # myUser = User("@jeffbezo", "12345678", "Jeffrey", "Bezo", country = "Amazon")
    # pprint(User.findItem("@whansel"))
    # pprint(User.findItem("@Mark"))
    for doc in User._DBCOLLECTION.find():
        pprint(doc)