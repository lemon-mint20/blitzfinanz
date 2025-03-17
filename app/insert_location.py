from pymongo import MongoClient
from datetime import datetime, timezone
import pytz
import os

containername = os.getenv("MONGO_CONTAINER_NAME", "mongo")
username = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
password = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin")

try:
    myclient = MongoClient(
        "mongodb://"+containername+":27017/",
        username=username,
        password=password) #Mongo URI format
    mydb = myclient["blitzfinancedb"]
except Exception as e:
    print("Error in connection:", e)

try:
    document = {
        "coordinates": {
            "type": "Point",
            "coordinates": [50.941382, 6.939854]
        },
        "name": "MARKET Sued",
        "company": "",
    }

    mydb["locations"].insert_one(document)
except Exception as e:
    print("Error in insertion:", e)
else:
    print("Data inserted successfully")