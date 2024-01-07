"""
This module contains DB configurations.
"""

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values


# Load configuration from .env file
CONFIG = dotenv_values(".env")

# Production MongoDB configuration
CLIENT = MongoClient(CONFIG["ATLAS_URI"], server_api=ServerApi("1"))
DB_NAME = CONFIG["DB_NAME"]
DB = CLIENT[DB_NAME]

USERS = DB["user"]
CANDIDATES = DB["candidate"]

USERS.create_index([("email", 1)], unique=True)
CANDIDATES.create_index([("email", 1)], unique=True)

# Test MongoDB configuration
TEST_CLIENT = MongoClient(CONFIG["TEST_ATLAS_URI"], server_api=ServerApi("1"))
TEST_DB_NAME = CONFIG["TEST_DB_NAME"]
TEST_DB = TEST_CLIENT[TEST_DB_NAME]

TEST_USERS = TEST_DB["user"]
TEST_CANDIDATES = TEST_DB["candidate"]

TEST_USERS.create_index([("email", 1)], unique=True)
TEST_CANDIDATES.create_index([("email", 1)], unique=True)

# Production flag
PRODUCTION = CONFIG["PRODUCTION"].lower().strip()

# Application level configurations
SECRET_KEY = CONFIG["SECRET_KEY"]
ALGORITHM = CONFIG["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"])