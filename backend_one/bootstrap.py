from flask import Flask
from src.bd.database import db
from src.config.config import Configuration as config
from src.app_module.app_router import router
import os

app = Flask(__name__)
app.register_blueprint(router)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQL_MODIFICATOR
app.secret_key = os.getenv('SECRET_KEY', 'super secret key')
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
        app.run(debug=bool(config.DEBAG), host="0.0.0.0", port=int(os.getenv("PORT", 5004)))