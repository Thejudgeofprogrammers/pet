from flask import Blueprint, redirect, render_template, request, url_for, flash
from datetime import datetime
from src.app_module.app_service import Services as service


router = Blueprint('router', __name__, template_folder='../../templates')


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
