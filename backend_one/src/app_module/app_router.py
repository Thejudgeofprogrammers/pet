from flask import Blueprint, redirect, render_template, request, url_for, flash, make_response, jsonify
from datetime import datetime
from src.app_module.app_service import Services as service
from uuid import uuid4
from src.bd.database import Operator, db
import redis
import os
from dotenv import load_dotenv
import requests as rq
load_dotenv('../../.env')

router = Blueprint('router', __name__, template_folder='../../templates')

client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis_server"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0
)

@router.before_request
def log_request():
    user_token = request.cookies.get('user_token')
    if not user_token:
        resp = make_response()
        resp.set_cookie('user_token', str(uuid4()))
        return resp
    return None

@router.before_request
def rights():
    if request.path == "/opdashboard":
        manager_token = request.cookies.get('manager_token')
        if manager_token and client.get(manager_token) == b'1':
            return None
        return redirect('/oplog')
    return None

@router.route('/')
def index():
    return render_template('index.html')


@router.route('/', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        surname = request.form.get('surname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        date = datetime.now().date()

        service.submit(name=name, surname=surname, phone=phone, email=email, date=date)
        flash("Форма успешно отправлена!", "success")

    except Exception as e:
        flash(f"Ошибка: {e}", "danger")

    return redirect('/')


@router.route('/add_video', methods=['GET', 'POST'])
def add_video():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            video_url = request.form['video_url']

            service.add_video(title=title, description=description, video_url=video_url)
            flash("Видео успешно добавлено!", "success")

            return redirect(url_for('videos_list'))
        
        except Exception as e:
            flash(f"Ошибка: {e}", "danger")
        
        return redirect(url_for('videos_list'))
    return render_template('add_video.html')


@router.route('/obychenie')
def videos_list():
    try:
        videos = service.videos_list()
        return render_template('obychenie.html', videos=videos)
    except Exception as e:
        flash(f"Ошибка загрузки видео: {e}", "danger")
        return redirect('/')


@router.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            
            service.add_article(title=title, description=description)
        
        except Exception as e:
            flash(f"Ошибка: {e}", "danger")
        
        return redirect(url_for('articles_list'))
    return render_template('add_article.html')


@router.route('/articles')
def articles_list():
    try:
        articles = service.articles_list()
        return render_template('articles.html', articles=articles)
    except Exception as e:
        flash(f"Ошибка загрузки статей: {e}", "danger")
        return redirect('/')


@router.route("/requests")
def view_notes():
    try:
        requests = service.view_notes()
        return render_template("requests.html", h1="Запросы", requests=requests)
    except Exception as e:
        flash(f"Ошибка загрузки запросов: {e}", "danger")
        return redirect('/')

@router.route('/oplog', methods=['GET', 'POST'])
def oplog():
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        req = rq.post('http://auth_service:5006/oplog', json={"login": login, "password": password})
        data = req.json()
        if data.get("allow"):
            resp = make_response(redirect('/opdashboard'))
            uid = str(uuid4())
            resp.set_cookie(key='manager_token', value=uid, httponly=False) # TTL # HTTPONLY # Secure
            client.set(name=uid, ex=int(os.getenv("TTL_COOKIE", 14400)), value="1") # TTL
            return resp
        return jsonify({"message": "Ошибка not allow"}), 403
    return render_template('oplog.html')

@router.route('/logout', methods=['POST'])
def logout():
    manager_token = request.cookies.get('manager_token')
    
    if manager_token:
        client.delete(manager_token)

    resp = make_response(redirect('/oplog'))
    resp.delete_cookie("manager_token")
    
    return resp

@router.route('/opdashboard')
def op_dashboard():
   return render_template('opdashboard.html')

# @router.route('/oplogout')
# @login_required
# def oplogout():
#    logout_user()
#    return redirect(url_for('oplog.html'))

# class Operator(UserMixin):
#     def __init__(self, id):
#         self.id = id

# @login_manager.user_loader
# def load_user(op_id):
#     return Operator(op_id) if client.exists(f"op:{op_id}") else None
    
    

# client.set('operators', 'admin', '12345')  # Логин: admin, Пароль: 12345