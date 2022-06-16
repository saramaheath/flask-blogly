"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import connect_db, User, db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
#debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.get('/')
def redirect_to_users():
    """List users and show add form"""

    return redirect('/users')
    

@app.get('/users/new')
def show_add_user_form():
    """ Display the form to add a user """
    return render_template('list.html')

@app.post('/add-user')
def create_display_user():
    """ Creates a user and displays that user's info """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    #user = User(first_name=first_name, last_name=last_name, image_url= image_url)
    user = User(
        first_name=first_name,
        last_name=last_name, 
        image_url=image_url
    )

    db.session.add(user)
    db.session.commit()

    return render_template('user.html', user=user)

@app.get('/users')
def list_users():
    """List users and show add form"""

    users = User.query.all()
    return render_template('current-users.html', users=users)

@app.get('/user/<int:id>')
def display_user(id):
    """displays user details"""

    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)

@app.get('/user/<int:id>/edit')
def display_edit_user(id):
    """displays user edit page"""
    user = User.query.get_or_404(id)
    return render_template('edit.html', user=user)


@app.post('/user/<int:id>/edit')
def update_user(id):
    """ updating user details and render the users page"""
    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()
    return render_template('user.html', user=user)
    

@app.post('/user/<int:id>/delete')
def delete_user(id):
    """ delete user and redirects to home page """
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
