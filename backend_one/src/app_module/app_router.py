from flask import Blueprint, redirect, render_template, request, url_for, flash, make_response
from datetime import datetime
from src.app_module.app_service import Services as service
from uuid import uuid4
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from src.bd.database import Operator, db
import redis
import os
from dotenv import load_dotenv

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
        login = request.form.get('login')
        password = request.form.get('password')

        # достаём из бд login password и сравниваем
        # достаём id из бд по логину
        # закидываем в редис operator_id
        # закидываем в cookie operator_id httpOnly
        # Сравниваем на странице op_dashboard
        
        
    return render_template('oplog.html')

# @router.route('/opdashboard')
# @login_required
# def op_dashboard():
#    return render_template('opdashboard.html')

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