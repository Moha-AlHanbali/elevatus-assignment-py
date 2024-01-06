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
CANDIDATES = DB["candidate"]

USERS.create_index([("email", 1)], unique=True)
CANDIDATES.create_index([("email", 1)], unique=True)


TEST_CLIENT = MongoClient(CONFIG["TEST_ATLAS_URI"], server_api=ServerApi("1"))
TEST_DB_NAME = CONFIG["TEST_DB_NAME"]
TEST_DB = TEST_CLIENT[TEST_DB_NAME]

TEST_USERS = TEST_DB["user"]
TEST_CANDIDATES = TEST_DB["candidate"]

TEST_USERS.create_index([("email", 1)], unique=True)
TEST_CANDIDATES.create_index([("email", 1)], unique=True)

PRODUCTION = CONFIG["PRODUCTION"]
