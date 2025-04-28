from pymongo import MongoClient
from src.db.models.chat_model import ChatModel
import os
from dotenv import load_dotenv

load_dotenv('../../.env')


MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo_db:27017")
client = MongoClient(MONGO_URI)
db = client[os.getenv('DATABASE_NAME_MONGO', 'my_db')]

message_collection = db["message"]
chats_collection = db["chats"]

def save_chat_to_db(chat: ChatModel):
    chat_dict = chat.model_dump()

    result = chats_collection.insert_one(chat_dict)

    return result.inserted_id