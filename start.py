from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
import os.path
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    base_dir, 'test.db')
app.config['JWT_SECRET_KEY'] = 'my-ulti-secret'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'c3bdc75b9740a9'
app.config['MAIL_PASSWORD'] = 'ca06acf28f7b5c'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#Initiating the config objects
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)
