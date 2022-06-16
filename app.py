"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import connect_db, User, db, DEFAULT_IMAGE_URL, Post
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
    return render_template('add-user-form.html')


@app.post('/add-user')
def create_display_user():
    """ Creates a user and displays that user's info """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] if request.form['image_url'] else DEFAULT_IMAGE_URL

    #user = User(first_name=first_name, last_name=last_name, image_url= image_url)
    user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )

    db.session.add(user)
    db.session.commit()
    posts = user.posts

    return render_template('user.html', user=user, posts=posts)


@app.get('/users')
def list_users():
    """List users and show add form"""

    users = User.query.all()
    return render_template('current-users.html', users=users)


@app.get('/user/<int:id>')
def display_user(id):
    """displays user details"""

    user = User.query.get_or_404(id)
    posts = user.posts
    return render_template('user.html', user=user, posts=posts)


@app.get('/user/<int:id>/edit')
def display_edit_user(id):
    """displays user edit page"""
    user = User.query.get_or_404(id)
    return render_template('edit-user.html', user=user)


@app.post('/user/<int:id>/edit')
def update_user(id):
    """ updating user details and render the users page"""
    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] if request.form['image_url'] else DEFAULT_IMAGE_URL

    db.session.commit()
    posts = user.posts

    return render_template('user.html', user=user, posts=posts)


@app.post('/user/<int:id>/delete')
def delete_user(id):
    """ delete user and redirects to home page """
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.get('/add-post/<int:id>')
def display_add_post_form(id):
    """ Displays the form to add posts """
    user = User.query.get_or_404(id)
    return render_template('add-post-form.html', user=user)


@app.post('/add-post/<int:id>')
def add_display_post(id):
    """ Adds the post and displays it's page """
    title = request.form['title']
    content = request.form['content']

    post = Post(
            title = title,
            content = content,
            created_at = None,
            user_id = id
    )

    user = User.query.get_or_404(id)

    db.session.add(post)
    db.session.commit()

    return render_template('post.html', user=user, post=post)

@app.get('/posts/<int:id>')
def display_post(id):
    """displays post details"""

    post = Post.query.get_or_404(id)
    user = post.user
    return render_template('post.html', post=post, user=user)

@app.post('/posts/<int:id>/edit')
def update_post(id):
    """ updating post details and render the posts page"""
    
    post = Post.query.get_or_404(id)
    user = post.user
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()
    return render_template('post.html', post=post, user=user)

@app.post('/posts/<int:id>/delete')
def delete_post(id):
    """ delete post and redirects to users page """
    post = Post.query.get_or_404(id)
    user = post.user

    db.session.delete(post)
    db.session.commit()
    posts = user.posts
    return render_template('user.html', user=user, posts=posts)

@app.get('/posts/<int:id>/edit')
def display_edit_post_form(id):
    """ displays edit post form """

    post = Post.query.get_or_404(id)

    return render_template('edit-post.html', post=post)