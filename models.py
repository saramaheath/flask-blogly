"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
DEFAULT_IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/commons/1/1a/Donkey_in_Clovelly%2C_North_Devon%2C_England.jpg'


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    first_name = db.Column(
        db.String(20),
        nullable=False
    )
    last_name = db.Column(
        db.String(20),
        nullable=False
    )
    image_url = db.Column(
        db.String(1000)
    )


def connect_db(app):
    """ Connects to database """
    db.app = app
    return db.init_app(app)
