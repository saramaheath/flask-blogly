"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from app import app


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
        db.String(200)
    )

    