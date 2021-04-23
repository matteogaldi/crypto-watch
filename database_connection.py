import os

import pymongo
from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
database = client["cryptoWatch"]


def save_data(collection, data):
    database[collection].insert_one(data)
