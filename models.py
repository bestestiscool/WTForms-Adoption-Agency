from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, URL, NumberRange, AnyOf

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Pet(db.Model):
    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)

    species = db.Column(db.String(10), nullable=False)

    photo_url = db.Column(db.String(250), nullable=True)

    age = db.Column(db.Integer, nullable=True)

    notes = db.Column(db.String(500), nullable=True)

    available = db.Column(db.Boolean, nullable=False, default=True)
