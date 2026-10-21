from pymongo import AsyncMongoClient


def create_mongo_client(dsn: str) -> AsyncMongoClient:
    return AsyncMongoClient(dsn, serverSelectionTimeoutMS=3000)