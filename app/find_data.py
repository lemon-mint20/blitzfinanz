from pymongo import MongoClient
import os

def connect_to_mongo():

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
    else:
        print("Connected to MongoDB")
        return mydb


def get_last_datetime():
    mydb = connect_to_mongo()

    try:
        last_datetime = mydb["Transactions"].find_one(sort=[("dateTime", -1)])["dateTime"]
    except Exception as e:
        print("Error in finding last datetime:", e)
    else:
        return last_datetime

def get_locations():
    mydb = connect_to_mongo()

    try:
        locations = mydb["locations"].distinct("name")
    except Exception as e:
        print("Error in finding locations:", e)
    else:
        return locations

def get_avg_value(limit = 10):
    mydb = connect_to_mongo()

    try:
        # Assuming you have a MongoDB collection named 'transactions'
        collection = mydb['Transactions']
        pipeline = [
            {"$limit": limit},
            {"$group": {"_id": None, "avgValue": {"$avg": "$value"}}}
        ]
        result = list(collection.aggregate(pipeline))
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0.0
    else:
        if result:
            return result[0]['avgValue']
        return 0.0

def get_last_currency():
    mydb = connect_to_mongo()

    try:
        last_currency = mydb["Transactions"].find_one(sort=[("dateTime", -1)])["currency"]
    except Exception as e:
        print("Error in finding last currency:", e)
    else:
        return last_currency

def get_last_direction():
    mydb = connect_to_mongo()

    try:
        last_direction = mydb["Transactions"].find_one(sort=[("dateTime", -1)])["direction"]
    except Exception as e:
        print("Error in finding last direction:", e)
    else:
        return last_direction

def get_accounts():
    mydb = connect_to_mongo()

    try:
        accounts = mydb["account"].distinct("name")
    except Exception as e:
        print("Error in finding accounts:", e)
    else:
        return accounts

def get_last_account():
    mydb = connect_to_mongo()

    try:
        last_account = mydb["Transactions"].find_one(sort=[("dateTime", -1)])["account"]
    except Exception as e:
        print("Error in finding last account:", e)
    else:
        return last_account

def get_tags():
    mydb = connect_to_mongo()

    try:
        tags = mydb["tags"].distinct("name")
    except Exception as e:
        print("Error in finding tags:", e)
    else:
        return tags