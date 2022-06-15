"""Blogly application."""

from flask import Flask, render_template, request
from models import connect_db, User, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


from flask_debugtoolbar import DebugToolbarExtension

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.get('/')
def list_users():
    """List users and show add form"""

    users = User.query.all()
    return render_template('current-users.html', users=users)

@app.get('/add-user-form')
def show_add_user_form():
    """ Display the form to add a user """
    return render_template('list.html')

@app.post('/add-user')
def create_display_user():
    """ Creates a user and displays that user's info """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = User(first_name=first_name, last_name=last_name, image_url= image_url)
    db.session.add(user)
    db.session.commit()

    return render_template('user.html', user=user)
