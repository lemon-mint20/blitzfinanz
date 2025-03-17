from pymongo import MongoClient
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
        "name": "Groceries",
    }

    mydb["tags"].insert_one(document)
except Exception as e:
    print("Error in insertion:", e)
else:
    print("Data inserted successfully")