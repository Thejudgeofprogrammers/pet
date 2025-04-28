from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Article(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(200), nullable=False)
    description   = db.Column(db.Text, nullable=False)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)


class Video(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(200), nullable=False)
    description   = db.Column(db.Text, nullable=False)
    video_url     = db.Column(db.String(300), nullable=False)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)


class Request_user(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    date          = db.Column(db.Date, nullable=False)
    name          = db.Column(db.String(50), nullable=False)
    surname       = db.Column(db.String(50), nullable=False)
    phone         = db.Column(db.String(20), nullable=False)
    email         = db.Column(db.String(100), nullable=False)

class Operator(db.Model):
    id: int         = db.Column(db.Integer, primary_key=True)
    login: str      = db.Column(db.String(50), nullable=False)
    password: str   = db.Column(db.String(50), nullable=False)


    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Дата: {self.date}\n"
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Телефон: {self.phone}\n"
            f"Email: {self.email}\n"
        )

