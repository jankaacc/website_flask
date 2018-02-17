from flask import redirect, render_template, flash, url_for, abort, session, request


from wtforms import validators
import bcrypt
from slugify import slugify


from application import app
from application.blog.form import SetupForm
from application.blog.form import PostForm, CommentForm
from application import db, uploaded_images
from application.author.models import Author
from application.blog.models import Blog, Category, Post, Comment
from application.author.decorators import login_required, author_required


POST_PER_PAGE = 5


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    blog = Blog.query.first()
    if not blog:
        return redirect(url_for('setup'))
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POST_PER_PAGE, False)
    return render_template('blog/index.html',blog=blog,posts=posts)


@app.route('/admin')
@app.route('/admin/<int:page>')
@author_required
def admin(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, POST_PER_PAGE, False)
    author = Author.query.filter_by(user_id = session['author_id']).first()

    for post in author.posts:
        print(post.title)

    if session['is_author']:
        return render_template('blog/admin.html', posts=posts, author=author)
    else:
        abort(403)


@app.route('/setup', methods=("POST","GET"))
def setup():
    form = SetupForm()
    error = ""
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author = Author(
             form.fullname.data,
             form.email.data,
             form.username.data,
             hashed_password,
             True
             )
        db.session.add(author)
        db.session.flush()
        if author.user_id:
            blog = Blog(
                form.name.data,
                author.user_id
                )
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = "Error creating user"
        if author.user_id and blog.id:
            db.session.commit()
            flash("Blog created")
            return redirect(url_for("index"))
        else:
            db.session.rollback()
            error = "Error creating blog"
    return render_template('blog/setup.html', form=form, error=error)


@app.route('/post', methods=('GET','POST'))
@author_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        filename = None
        if form.image.has_file():
            print("good")
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("image not uploaded")
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            category_slug = slugify(form.new_category.data)
            new_category.slug = category_slug
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        elif form.category.data:
            category_id = form.category.get_pk(form.category.data)
            category = Category.query.filter_by(id=category_id).first()
        else:
            category = None
        blog = Blog.query.first()
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        post = Post(blog,author,category,title,body,filename,slug)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', slug=slug))
    return render_template('blog/post.html', form=form, action='new')


@app.route('/article/<slug>', methods=('GET','POST'))
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post.id)

    if form.validate_on_submit():
        blog = Blog.query.first()
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data

        comment = Comment(blog, title, author, body)
        comment.post_id = post.id

        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article'))

    return render_template('blog/article.html', post=post, form=form)


@app.route('/delete/<int:post_id>')
@author_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash('Post has been deleated')
    return redirect('/admin')


@app.route('/edit/<int:post_id>', methods=('GET','POST'))
@author_required
def edit(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post)
    if form.validate_on_submit():
        original_image = post.image
        form.populate_obj(post)
        if form.image.has_file():
            image = request.files.get('image')
            filename = None
            try:
                filename = uploaded_images.save(image)
            except:
                flash("No picture updated")
            if filename:
                post.image = filename
        else:
            post.image = original_image
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            slug = slugify(new_category.name)
            new_category.slug = slug
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category
        db.session.commit()
        return redirect(url_for('article', slug=post.slug))
    return render_template('blog/post.html', form=form, post=post, action='edit')


@app.route('/category/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    posts = Post.query.filter_by(category_id=category.id )
    return render_template('blog/category.html', posts=posts, category=category )















