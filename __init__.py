from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '$@F!#GWWT#$^@#GWT#GWGWG'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kiet741852963@localhost/bookstore?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 10

cloudinary.config(
    cloud_name='dcwyrfw4i',
    api_key='348826818816533',
    api_secret='3YY4I1WT__6-NsdizlwpoZemmrY'
)

db = SQLAlchemy(app=app)


login = LoginManager(app=app)
