from application import db
from application import uploaded_images


class Author(db.Model):
   # __tablename__ = 'people'
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.Unicode)
    password = db.Column(db.String(60))  # ('password', db.Unicode)
    email = db.Column(db.String(35), unique=True)
    fullname = db.Column(db.String(80))
    is_author = db.Column(db.Boolean)
    intrests = db.Column(db.Text)
    image = db.Column(db.String(255))
    slug = db.Column(db.String(256), unique=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def imgsrc(self):
        return uploaded_images.url(self.image)

    def __init__(self, fullname, email, username, password ,image=None, intrests=None, is_author=False, slug=None):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.image = image
        self.intrests = intrests
        self.is_author = is_author
        #self.posts = posts
        self.slug = slug


    def __repr__(self):
        return '<Author %r>' % self.username
