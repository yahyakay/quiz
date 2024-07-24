import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/shop_db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/todos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
