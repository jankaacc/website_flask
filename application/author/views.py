from flask import render_template, redirect, url_for, session, request, flash


from slugify import slugify
import bcrypt


from application import app
from application.author.form import RegisterForm, LoginForm
from application.author.models import Author
from application.blog.models import Post
from application import db, uploaded_images
from application.author.decorators import login_required




@app.route('/login', methods=('GET','POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        authors = Author.query.filter_by(
            username = form.username.data,
            ).limit(1)
        if authors.count():
            author = authors[0]

            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                session['author_id'] = author.user_id
                flash('User {x} logged in'.format(x=form.username.data))
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else:
                error = 'Incorrect username and password'
        else:
            error = 'Incorrect username and password'
    return render_template('author/login.html', form=form, error=error)


@app.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm()

    if request.method == 'POST' and request.args.get('next'):
        session['next'] = request.args.get('next', None)
        print('good')
    if form.validate_on_submit():
        #image add for author
        filename = None
        if form.image.has_file():
            print("good")
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("image not uploaded")

        slug = slugify(form.username.data)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            filename,
            form.intrests.data,
            True,
            slug=slug
        )
        db.session.add(author)
        db.session.commit()
        if 'next' in session:
            next = session.get('next')
            session.pop('next')
            return redirect(next)
        else:
            return redirect(url_for('success'))
    return render_template('author/register.html', form=form)


@app.route('/success')
def success():
    return redirect('index')


@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_author')
    session.pop('author_id')
    return redirect(url_for('index'))


@app.route('/author/<slug>')
def author(slug):
    author_id = session.get('author_id')
    author = Author.query.filter_by(slug=slug).first_or_404()
    posts=Post.query.filter_by(author_id=author.user_id)

    print('done')
    for post in posts:
        print(post.title)
    return render_template('author/author.html', author=author, slug=author.slug)