from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_tests"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()
        

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           image_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_home_page(self):
        with self.client as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 302)

    def test_users_new(self):
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Add user page shown -->", html)

    def test_add_user(self):
        with self.client as c:
            resp = c.post(
                "/add-user",
                data={
                    'first_name': 'Jordan',
                    'last_name': 'Asano',
                    'image_url': ''}
            )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- User page shown -->", html)
            self.assertIn("Jordan Asano", html)

    def test_display_user(self):
        with self.client as c:
            resp = c.get(f"/user/{User.query.first().id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- User page shown -->", html)

    def test_display_edit_user(self):
        with self.client as c:
            resp = c.get(f"/user/{User.query.first().id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Edit user page shown -->", html)

    def test_edit_user(self):
        with self.client as c:
            user = User.query.first()
            resp = c.post(
                f"/user/{user.id}/edit",
                data={
                    'first_name': 'Sara',
                    "last_name": "Heath",
                    'image_url': ''}
            )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- User page shown -->", html)
            self.assertIn("Sara Heath", html)

    def test_delete_user(self):
        with self.client as c:
            user = User.query.first()
            resp = c.post(f"/user/{user.id}/delete")
            self.assertEqual(resp.status_code, 302)
            html = resp.get_data(as_text=True)
            self.assertIn('<a href="/">', html)

    def test_display_add_post_form(self):
        with self.client as c:
            user = User.query.first()
            resp = c.get(f"/add-post/{user.id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('<!-- Add post form shown -->', html)

    def test_add_post(self):
        with self.client as c:
            user = User.query.first()
            resp = c.post(
                f"/add-post/{user.id}",
                data={'title': 'Yo', 'content': 'hi'}
            )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('<!-- Post page shown -->', html)
            self.assertIn('Yo', html)
            self.assertIn('hi', html)

