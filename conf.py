from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv(verbose=True)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
client = MongoClient(DB_HOST, DB_PORT)
db = client[DB_NAME]