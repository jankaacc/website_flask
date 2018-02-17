from flask_wtf import Form
from flask_wtf.file import FileAllowed, FileField
from wtforms import validators, StringField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField


from application.author.form import RegisterForm
from application.blog.models import Category
from application import uploaded_images


class SetupForm(RegisterForm):
    name = StringField('Blog name',[
        validators.required(),
        validators.Length(max=80)
        ])

def categories():
    return Category.query


class PostForm(Form):
    image = FileField('Image', validators=[
                    FileAllowed(uploaded_images, 'Images only!')
                    ])
    title = StringField('Title',[
                        validators.required(),
                        validators.Length(max = 80)
                        ])
    body = TextAreaField('Content', validators=[validators.required()])
    category = QuerySelectField('Category', query_factory=categories, allow_blank=True)
    new_category = StringField('New Category')


class CommentForm(Form):
    title = StringField('Title', [
        validators.required(),
        validators.Length(max=80)
    ])
    body = TextAreaField('Content', validators=[validators.required()])
