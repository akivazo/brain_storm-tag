import pytest
from flask.testing import FlaskClient
from mongomock import MongoClient
from ..tag_api import server, set_mongo_client

@pytest.fixture
def client():
    mongo_client = MongoClient()
    set_mongo_client(mongo_client=mongo_client)
    server.config["TESTING"] = True
    client = server.test_client()
    yield client
    mongo_client.close()

def test_add_tags(client: FlaskClient):
    response = client.post("/tag/tech")
    assert response.status_code == 201
    assert response.get_json()["count"] == 1
    response = client.post("/tag/housing")
    assert response.status_code == 201
    response = client.post("/tag/travel")
    assert response.status_code == 201

def test_get_all_tags(client: FlaskClient):
    response = client.post("/tag/tech")
    assert response.status_code == 201
    response = client.post("/tag/housing")
    assert response.status_code == 201
    response = client.post("/tag/travel")
    assert response.status_code == 201
    response = client.post("/tag/housing")
    assert response.status_code == 201
    response = client.post("/tag/housing")
    assert response.status_code == 201
    response = client.post("/tag/tech")
    assert response.status_code == 201

    response = client.get("tags")
    tags = response.get_json()["tags"]

    assert tags == {"tech": 2, "housing": 3, "travel": 1} 

    response = client.post("/tag/food")
    assert response.status_code == 201

    response = client.get("tags")
    tags = response.get_json()["tags"]

    assert tags == {"tech": 2, "housing": 3, "travel": 1, "food": 1} 

def test_no_tags(client: FlaskClient):

    response = client.get("tags")
    tags = response.get_json()["tags"]
    
    assert tags == {}
