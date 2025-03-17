from pymongo import MongoClient
from datetime import datetime, timezone
import pytz
import os

def connect_to_mongo():
    containername = os.getenv("MONGO_CONTAINER_NAME", "mongo")
    username = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
    password = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin")

    try:
        myclient = MongoClient(
            "mongodb://"+containername+":27017/",
            username=username,
            password=password)  # Mongo URI format
        mydb = myclient["blitzfinancedb"]
    except Exception as e:
        print("Error in connection:", e)
    else:
        print("Connected to MongoDB")
        return mydb

def insert_transaction(dateTime, timezone, location, value, currency, direction, description, account, tags, receipt):
    mydb = connect_to_mongo()

    try:
        localized_timezone = pytz.timezone(timezone)
        dateTime = localized_timezone.localize(datetime.strptime(dateTime, "%Y-%m-%dT%H:%M:%S")).isoformat()

        document = {
            "dateTime": dateTime,
            "location": set_location_by_match(location),
            "value": float(value),
            "currency": currency,
            "direction": direction,
            "description": description,
            "account": account,
            "tags": tags,
            "receipt": receipt
        }

        # Insert the document
        mydb["Transactions"].insert_one(document)
        print("Data inserted successfully")
    except Exception as e:
        print("Error in insertion:", e)
        raise e


def set_location_by_match(location_string):
    mydb = connect_to_mongo()

    try:
        # Find by matching string in name field of locations collection
        location = mydb["locations"].find_one({"name": {"$regex": location_string, "$options": "i"}})
    except Exception as e:
        print("Error in finding locations:", e)
    else:
        print(f"Found: {location}")
        return location["_id"]