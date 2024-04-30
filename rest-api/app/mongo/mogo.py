import pymongo
from typing import Any

collection: Any
def init_mongo():
    global collection
    client = pymongo.MongoClient("mongodb://mongo:27017/")
    db = client["biome-club"]
    collection = db["market"]

def get_market():
    return collection