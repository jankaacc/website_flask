import os


SECRET_KEY = 'you-will-never-guess'
DEBUG=True


DB_USERNAME = 'postgres'
DB_PASSWORD = 'eye9rpou'#'test'#
BLOG_DATABASE_NAME = 'users'#'blog'
DB_HOST = 'localhost:5432'#'postgres:5432'
DB_URI = "postgresql://%s:%s@%s/%s" %(DB_USERNAME,DB_PASSWORD,DB_HOST,BLOG_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_IMAGES_DEST = '/home/jankaacc/repos/second_website_flask/application/static/images/'#'/opt/flask_blog/application/static/images'#
UPLOADED_IMAGES_URL = '/static/images/'