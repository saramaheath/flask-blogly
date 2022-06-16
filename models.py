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
        db.String(1000),
        nullable=False,
        default=''
    )

    posts = db.relationship('Post',
                            backref='user')


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.now()
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )


def connect_db(app):
    """ Connects to database """
    db.app = app
    return db.init_app(app)
