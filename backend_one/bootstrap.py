from flask import Flask
from src.bd.database import db
from src.config.config import Configuration as config
from http.cookies import SimpleCookie
from src.app_module.app_router import router
import os
from uuid import uuid4

app = Flask(__name__)
app.register_blueprint(router)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQL_MODIFICATOR


def middleware_one(app):
    def middleware(environ, start_response):
        cookies = SimpleCookie(environ.get('HTTP_COOKIE', ''))
        user_token = cookies.get('user_token')

        def custom_start_response(status, headers, exc_info=None):
            if user_token is None:
                user_id = str(uuid4())
                ttl = int(os.getenv("TTL_COOKIE", 60 * 60 * 24))
                headers.append((
                    'Set-Cookie',
                    f'user_token={user_id}; Max-Age={ttl}; Path=/;'
                ))
            return start_response(status, headers, exc_info)

        return app(environ, custom_start_response)
    return middleware

app.wsgi_app = middleware_one(app.wsgi_app)

if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
        app.run(debug=bool(config.DEBAG), host="0.0.0.0", port=int(os.getenv("PORT", 5004)))