from unittest import TestCase
from flask import Flask
from models import db, User, Post
from app import app 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
app.config['TESTING'] = True

class TestApp(TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        

    def testRoot(self):
        """test redirect to users"""

        # test response code
        response = self.client.get('/')
        self.response.assertEqual(response.status_code, 302)


    def testShowNewUser(self):
        """test route to '/users'"""

        # test response code
        response = self.client.get('/users')
        self.response.assertEqual(response.status_code, 200)


    def testUserIndex(self):
        """test show users from db"""

        # add test user to db
        user1 = User(first_name='John', last_name='Doe')
        user2 = User(first_name='Jane', last_name='Smith')

        db.session.add_all([user1, user2])
        db.session.commit()

        # test response code
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

       # test user exists in response data
        self.assertIn('John Doe', response.get.data(as_text = True)) 
        self.assertIn('Jane Smith', response.get.data(as_text = True))


    def testNewUser(self):
        """test additon of user to db"""

        # send user data to db and test response code
        response = self.client.post('/users/new', data={'first_name':'Alice', 'last_name':'Johnson'})
        self.response.assertEqual(response.status_code, 302)

        #test data was sent to db
        user = User.query.filter_by(first_name='Alice', last_name='Johnson').first()
        self.assertIsNone(user)

    
    def testDeleteUser(self):
        """test deltion of user existing in db"""

        # add test user to db
        user = User(first_name='Ronald', last_name='McDonald')
        db.session.add(User)
        db.session.commit()

        #send delete request and test response code
        response = self.client.post(f'/users/{user.id}/delete')
        self.assertEqual(response.status_code, 302)

        #test user no longer exists in db
        deleted_user = User.query.get(user.id)
        self.assertIsNone(user)


    def testnewPost(self):
        """test post is sent to db correctly"""

        response = self.client.post('user/1/posts/new', data={
            'title': 'post title',
            'content': 'some post content' 
        }, follow_redirects =True)

        self.assertEqual(response.status_code, 200)

        post = Post.query.filter(post.title== 'post title')
        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'some post content')