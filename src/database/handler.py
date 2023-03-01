import os
from typing import Any, Mapping

from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.database import Database

load_dotenv()

CONNECTION_STRING = os.getenv('MONGODB_URI')
client = MongoClient(CONNECTION_STRING)

def getDb():
    return client
