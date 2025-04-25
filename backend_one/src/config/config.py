import os
from dotenv import load_dotenv

load_dotenv()

class Configuration:
    DB_URL = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    SQL_MODIFICATOR = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    DEBAG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
