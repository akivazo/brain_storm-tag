from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from typing import Type, List

server = Flask(__name__)
CORS(server)
tag_collection = None

def set_mongo_client(mongo_client: MongoClient):
    global tag_collection
    tag_collection = mongo_client.get_database("brain_storm").get_collection("tag")

@server.route("/")
def index():
    return "Tags API"

@server.route("/tags", methods=["GET"])
def get_all_tags():
    tags = tag_collection.find()
    result = {}
    for tag in tags:
        result[tag["Name"]] = tag["Count"]
    return jsonify({"tags": result})
    

@server.route("/tag/<name>", methods=["POST"])
def add_tag(name):
    tag = tag_collection.find_one({"Name": name})
    if tag:
        # increaase count by one
        count = tag["Count"]
        count += 1
        tag_collection.update_one({"Name": name}, {"$inc": {"Count": 1}})
    else:
        tag_collection.insert_one({"Name": name, "Count": 1})
    return jsonify("Tag was added succefully"), 201


if __name__ == "__main__":
    import os, dotenv
    dotenv.load_dotenv()
    mongo_client = MongoClient(os.environ["TAG_MONGODB_URI"])
    set_mongo_client(mongo_client)
    server.run(debug=True, port=5000)
    mongo_client.close()