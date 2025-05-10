import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_socketio import SocketIO, send, emit
from dotenv import load_dotenv
import os
from src.db.init_db import message_collection, chats_collection
from src.db.models.message_model import Message
from src.db.models.chat_model import ChatModel
import redis
from bson import ObjectId
import datetime

def json_serializable(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
socketio = SocketIO(app, async_mode='eventlet', path='/ws/socket.io', cors_allowed_origins="*")

client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis_server"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0
)

@socketio.on('connect')
def handle_connect(auth=None):
    print('Connected')
    user_token = request.cookies.get("user_token")
    chat_token = request.cookies.get("chat_token")
    if not user_token:
        print('user token not exists')
        return
    if not chat_token:
        chat = ChatModel(userid=user_token)
        chat_id = chat.chatid
        chats_collection.insert_one(chat.model_dump())
        
        emit('new_chat_token', {"chat_token": chat_id})

@socketio.on('new_chat_token')
def handle_new_chat(auth=None):
    user_token = request.cookies.get("user_token")
    chat = ChatModel(userid=user_token)
    chat_id = chat.chatid
    chats_collection.insert_one(chat.model_dump())
        
    emit('new_chat_token', {"chat_token": chat_id})

@socketio.on('new_message')
def handle_message(data):
    print('1')
    user_token = request.cookies.get("user_token")
    chat_token = request.cookies.get("chat_token")
    print('2')
    if not (user_token and chat_token):
        return
    print('3')
    message = Message(userid=user_token, text=data["text"])
    print('4')
    # Сериализация сообщения для MongoDB
    msg_dict = message.dict()  # Используем dict() для правильной сериализации Pydantic объекта
    msg_dict = {k: (v.isoformat() if isinstance(v, datetime.datetime) else v) for k, v in msg_dict.items()}
    print('5')
    # Сохраняем сообщение в коллекцию чатов
    chat = chats_collection.find_one_and_update(
        {"chatid": chat_token},
        {"$push": {"messages": msg_dict}},
        return_document=True
    )
    print('6')
    if not chat:
        print(f"Ошибка: чат с id {chat_token} не найден!")
        return
    print('7')
    emit('new_message', msg_dict, broadcast=True)

@socketio.on('load_messages')
def handle_load_messages():

    chat_token = request.cookies.get("chat_token")
    
    if not chat_token:
        print("chat_token отсутствует в куках")
        emit('load_messages', [])  # или отправить ошибку на клиент
        return

    print(chat_token)
    chat = chats_collection.find_one({"chatid": chat_token})
    print(chat)
    if not chat:
        print(f"Чат с id {chat_token} не найден, создаем новый")
        chat = {
            "chatid": chat_token,
            "messages": [] 
        }
        chats_collection.insert_one(chat)
    messages = chat.get("messages", [])
    print(messages)
    serializable_messages = [
        {k: json_serializable(v) for k, v in msg.items()}
        for msg in messages
    ]
    print(serializable_messages)
    emit('load_messages', serializable_messages)

@socketio.on('get_all_chats')
def handle_get_all_chats():
    user_token = request.cookies.get("user_token")

    if not user_token:
        emit('all_chats', {"error": "user_token is missing"})
        return

    chats = list(chats_collection.find({"userid": user_token}))

    for chat in chats:
        chat["_id"] = str(chat["_id"])  # Преобразуем ObjectId
        chat["chatid"] = str(chat["chatid"])
        chat["messages"] = [
            {k: json_serializable(v) for k, v in msg.items()}
            for msg in chat.get("messages", [])
        ]

    emit('all_chats', {"chats": chats})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

    
if __name__ == "__main__":
    socketio.run(app, debug=bool(os.getenv('DEBUG', False)), host="0.0.0.0", port=int(os.getenv("PORT", 5005)))
