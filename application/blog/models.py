from datetime import datetime

from application import db, uploaded_images

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.user_id'))
    posts = db.relationship('Post', backref='blog', lazy='dynamic')

    def __init__(self, name, admin):
        self.name = name
        self.admin = admin

    def __repr__(self):
        return '<Blog %r>' %self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    author_id =  db.Column(db.Integer, db.ForeignKey('author.user_id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(255))
    slug = db.Column(db.String(256), unique=True)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    comments = db.relationship('Comment',order_by="desc(Comment.id)" ,backref='post', lazy='dynamic')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    @property
    def imgsrc(self):
        return uploaded_images.url(self.image)

    def __init__(self, blog, author, cathegory, title, body, image=None ,slug=None, publish_date=None, live=True):
        self.blog_id = blog.id
        self.author_id = author.user_id
        self.title = title
        self.body = body
        self.image = image
        self.slug = slug
        self.category_id = cathegory.id
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date
        self.live = live

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String(256), unique=True)

    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, name, slug=None):
        self.name = name
        self.slug = slug

    def __repr__(self):
        return '<Category %r>' % self.name


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.user_id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, blog, title, author, body, publish_date=None, live=True):
        self.blog_id = blog.id
        self.title = title
        self.body = body
        self.author_id = author.user_id

        if publish_date is None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date
        self.live = live

    def __repr__(self):
        return '<Comment %r>' % self.title




