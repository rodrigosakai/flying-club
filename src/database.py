"""
Database module
"""
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongomock import MongoClient as MockMongoClient
from src import date

ENV = os.getenv("ENV")
DATABASE = os.getenv("DATABASE", "flying-club")

if ENV == "production":
    HOST = os.getenv("HOST")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    if None in (HOST, USER, PASSWORD, DATABASE):
        raise RuntimeError("Database config not set up")

    client = MongoClient(f"mongodb+srv:///{USER}:{PASSWORD}@{HOST}/{DATABASE}")

elif ENV == "testing":
    client = MockMongoClient()

db = client.get_database(DATABASE)


def get_documents(collection: str, query: dict = None) -> list:
    """
    Returns documents from database

    Params:
    -------
    collection: str
        Name of collection
    query: dict (default None)
        Filter query

    Returns:
    -------
    list: list of documents
    """
    return list(db.get_collection(collection).find(query))


def insert_document(document: dict, collection: str):
    """
    Inserts document into database

    Params:
    -------
    document: dict
        Document in a dict format
    collection: str
        Name of the collection

    Returns:
    -------
    object_id: str
        ID of the inserted document
    timestamp: str
    """
    document["created_at"] = date.get_current_timestamp()
    result = db.get_collection(collection).insert_one(document)

    document_id = result.inserted_id
    created_at = document["created_at"]

    del document["created_at"]

    return document_id, created_at


def update_document(document_id: str, collection: str, update_fields: dict) -> str:
    """
    Update document in database

    Params:
    -------
    document_id: str
        ID of document
    collection: str
        Collection in which the document is
    update_fields: dict
        Fields to be updated

    Returns:
    -------
    timestamp: str
    """
    update_fields_minus_id = {
        key: update_fields[key] for key in update_fields if key != "_id"}
    update_fields_minus_id["updated_at"] = date.get_current_timestamp()

    db.get_collection(collection).update_one(
        {"_id": ObjectId(document_id)},
        {"$set": update_fields_minus_id}
    )

    return update_fields_minus_id["updated_at"]
