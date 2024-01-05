'This module contains DB configs'

from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")

CLIENT = MongoClient(CONFIG["ATLAS_URI"], server_api=ServerApi("1"))
DB_NAME = CONFIG["DB_NAME"]
DB = CLIENT[DB_NAME]
USERS = DB["user"]

USERS.create_index([("email", 1)], unique=True)
