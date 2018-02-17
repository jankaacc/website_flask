#Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask import Flask
import tempfile
import unittest
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy


from application import app, db


#models
from application.author.models import *
from application.blog.models import *


class UserTest(unittest.TestCase):
    def setUp(self):
        db_username = app.config['DB_USERNAME']
        db_password = app.config['DB_PASSWORD']
        db_host = app.config['DB_HOST']
        self.db_uri = "postgresql://%s:%s@%s/" % (db_username, db_password, db_host)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['BLOG_DATABASE_NAME'] = 'test_blog'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
        db.create_all()
        self.app = app.test_client()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def create_blog(self):
        return self.app.post('/setup', data=dict(
            name='My Test Blog',
            fullname='Jan Mk',
            email='j.s@gmail.com',
            username='jorge',
            password='test',
            confirm='test'
        ),
        follow_redirects = True)


    def test_create_blog(self):
        rv = self.create_blog()
        assert 'Blog created' in str(rv.data)


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ),
            follow_redirects=True)


    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    def test_login_logout(self):
        self.create_blog()
        rv = self.login('jorge','test')
        assert 'User jorge logged in' in str(rv.data)


if __name__ == '__main__':
     unittest.main()