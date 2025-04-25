from flask import Flask, request, make_response
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
import os
from src.db.init_db import message_collection, chats_collection
from src.db.models.message_model import Message
from src.db.models.chat_model import ChatModel
import redis
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
socketio = SocketIO(app, async_mode='eventlet')

client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis_server"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0
)

@socketio.on('connect')
async def handle_connect():
    user_token = request.cookies.get("user_token")
    chat_token = request.cookies.get("chat_token")

    # Если у пользователя нет chat_token, создаем новый чат
    if not chat_token and user_token:
        # Создаем новый chat_token для этого пользователя
        chat = ChatModel(userid=user_token)
        chat_id = chat.chatid
        
        # Сохраняем новый чат в базу данных
        await chats_collection.insert_one(chat.dict())
        
        # Сохраняем chat_token в cookies
        resp = make_response()
        resp.set_cookie('chat_token', chat_id, max_age=72000, httponly=False)
        
        # Отправляем chat_token в cookies и отправляем на клиент
        send({"chat_token": chat_id})

@socketio.on('message')
async def handle_message(data):
    # data = {"text": "Привет"}
    user_token = request.cookies.get("user_token")
    chat_token = request.cookies.get("chat_token")

    if not (user_token and chat_token):
        return

    message = Message(userid=user_token, text=data["text"])
    
    # Добавим в базу данных
    await chats_collection.update_one(
        {"chatid": chat_token},
        {"$push": {"messages": message.dict()}}
    )

    send(message.dict(), broadcast=True)

@socketio.on('load_messages')
async def handle_load_messages():
    chat_token = request.cookies.get("chat_token")

    chat = await chats_collection.find_one({"chatid": chat_token})

    if not chat:

        print(f"Чат с id {chat_token} не найден, создаем новый")
        chat = {
            "chatid": chat_token,
            "messages": [] 
        }

        await chats_collection.insert_one(chat)

    send(chat.get("messages", []))

@socketio.on('disconnect')
async def handle_disconnect():
    print('Client Disconnected')

    

if __name__ == "__main__":
    socketio.run(app, debug=bool(os.getenv('DEBAG', False)), host="0.0.0.0", port=int(os.getenv("PORT", 5005)))
