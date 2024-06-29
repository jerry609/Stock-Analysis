import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:152189@localhost/stock'
    SQLALCHEMY_TRACK_MODIFICATIONS = False