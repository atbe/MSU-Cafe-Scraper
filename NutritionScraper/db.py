# Author: Ibrahim Ahmed

from pymongo import MongoClient
from NutritionScraper.NutritionApiTools import build_keywords_from_name
import json
import bson
# from NutritionScraper.NutritionApi import FoodItem

class MSUCafeDB(object):
    """
    Used to model our MongoDB connection instance.
    """
    db_connection = None

    def __init__(self, collection_name):
        """
        Create our db instance.
        """
        self.connection = MongoClient("mongodb://localhost:27017")
        self.database = self.connection['msu-cafe']
        self.collection = self.GetValidCollection(collection_name)

    def __del__(self):
        """
        Close the connection when we go out of scope.
        """
        self.connection.close()

    def SearchForFoodItem(self, search_term, single_result=True, same_keyword_length=False):
        """
        Enter the exact name of the food item as is:

        'Vegetable Fried Rice'
        'Breadsmith's Bakery Dinner Roll'

        :param search_term:
        :return:
        """
        keywords = build_keywords_from_name(search_term)
        # print(keywords)
        # filters = [ for keyword in keywords}]
        filters = []
        for keyword in keywords:
            filters.append({'keywords': {"$in": [keyword]}})
        if same_keyword_length:
            tollerance = 1
            filters.append({'keywords': {"$size": len(keywords)}})
        search_query = {"$and" : filters}
        # print(search_query)
        if single_result:
            return self.collection.find_one(search_query)
        else:
            return self.collection.find(search_query)

    def InsertFoodItem(self, foodItem):
        # if not isinstance(foodItem, foodItem):
            # return

        print("DEBUG: MSUCafeDB(InsertFoodItem - inserting ", foodItem.name)
        self.collection.insert_one(foodItem.__dict__)

        # input("Press enter to continue")

    def AlreadyHaveFoodItem(self, food_name):
        return self.collection.find_one({'name': food_name}) != None

    def GetValidCollection(self, collection_name):
        """
        Checks if the collection exists.

        :param collection_name: Name of the collection to check.
        :return: True if the collection exists.
        """

        if collection_name in self.database.collection_names():
            return self.database[collection_name]
        else:
            raise ValueError(
                """The collection you requested ({}) does not exist in the database.
                Please ask your database admin to create the collection.""".format(collection_name))
