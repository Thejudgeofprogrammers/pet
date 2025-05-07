from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from uuid import uuid4
from pymongo import MongoClient
from pydantic import BaseModel, Field
load_dotenv()

# Создать пользователей при включении в env
# Endpoint load
## Cookie httpOnly manager_id

app = Flask(__name__)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo_db:27017")
client = MongoClient(MONGO_URI)
db = client[os.getenv('DATABASE_NAME_MONGO', 'my_db')]
manager_collection = db["managers"]


class Message(BaseModel):
    manager_id: str = Field(default_factory=lambda: str(uuid4()))
    manager_login: str
    password: str
    
    class Config:
        orm_mode = True


def check_service(login, password):
    if login == os.getenv("DEFAULT_MANAGER_LOGIN", "admin") and password == os.getenv("DEFAULT_MANAGER_PASSWORD", "admin"):
        return True
    
    manager = manager_collection.find_one({ "login": login })
    if not manager:
        return False
    if login == manager["login"] and password == manager["password"]:
        return True
    else:
        return False
    
def make_managers():
    if manager_collection.count_documents({}) == 0:
        manager_collection.insert_one({
            "login": os.getenv("DEFAULT_MANAGER_LOGIN", "admin"),
            "password": os.getenv("DEFAULT_MANAGER_PASSWORD", "admin")
        })

@app.route('/oplog', methods=['POST'])
def oplog():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Некорректный формат запроса"}), 400

    manager_login = data.get("login")
    password = data.get("password")
    
    print(manager_login)
    print(password)
    
    if check_service(manager_login, password):
        return jsonify({"allow": True}), 200
    print(check_service(manager_login, password))
    return jsonify({"message": "Не удалось войти"}), 403


if __name__ == "__main__":
    make_managers()
    app.run(debug=bool(os.getenv("DEBAG", False)), host="0.0.0.0", port=int(os.getenv("PORT", 5006)))
