from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from typing import Type, List

server = Flask(__name__)
CORS(server)
user_collection = None

def set_mongo_client(mongo_client: MongoClient):
    global user_collection
    user_collection = mongo_client.get_database("brain_storm").get_collection("tag")
    user_collection.insert_one({"name": "tags", "strings": []})

@server.route("/")
def index():
    return "Tags API"

@server.route("/tags", methods=["GET"])
def get_all_tags():
    result = user_collection.find_one({"name": "tags"}, {"_id": 0, "tags": 1})
    if result:
        return jsonify({"tags": result["tags"]})

@server.route("/tag/<name>", methods=["POST"])
def add_tag(name):
    user_collection.update_one({"name": "tags"}, {"$push": {"tags": name}}, upsert=True)
    return jsonify("Tag was added succefully"), 201


if __name__ == "__main__":
    import os, dotenv
    dotenv.load_dotenv()
    mongo_client = MongoClient(os.environ["TAG_MONGODB_URI"])
    set_mongo_client(mongo_client)
    server.run(debug=True, port=5000)
    mongo_client.close()