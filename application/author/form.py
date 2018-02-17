from flask_wtf import Form
from flask_wtf.file import FileAllowed, FileField
from wtforms import validators, StringField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField


from application import uploaded_images


class RegisterForm(Form):
    image = FileField('Image', validators=[
        FileAllowed(uploaded_images, 'Images only!')
    ])
    fullname = StringField('Full Name', [validators.required()])
    email = EmailField('Email',[validators.required()])
    username = StringField('Username', [
        validators.required(),
        validators.Length(min=4, max=25),
        ])
    password = PasswordField('New Password', [
        validators.required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')
    intrests = TextAreaField('Intrests')


class LoginForm(Form):
    username = StringField('Username', [
        validators.required(),
        validators.Length(min=4, max=25),
        ])
    password = PasswordField('Password', [
        validators.required(),
        validators.Length(min=4, max=25),
        ])