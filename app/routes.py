
from crypt import methods
from os import abort
from flask import render_template, url_for, redirect, request, abort
from app.forms import RegForm, LogForm, Comment
from app import app, db, bcrypt
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# @TODO: Basic homePage route 
@app.route('/')
def home():
    title = 'HomePage'
    posts = Post.query.all()
    return render_template('home.html', title = title, posts = posts)


# @TODO: Register route 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', title ='Register', form = form)

# @TODO: Login route 
@app.route('/login' , methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LogForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    
    return render_template('login.html', title ='Login', form = form)

# @TODO: Logout route 
@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('home'))

# @TODO: Profile route 
@app.route('/profile')
@login_required
def profile():

    title = 'User Account'
    return render_template('profile.html', title = title)

# @TODO: Create Post 
@app.route('/post/new', methods=['GET', 'POST'])
def post_new():
    form = Comment()
    if form.validate_on_submit():
        post = Post(title = form.post_title.data, content = form.post_content.data, author = current_user)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('post.html',legend='Create Post', form = form)

# @TODO: Get Single Post
@app.route('/single-post/<int:post_id>')
@login_required
def single_post(post_id):
    title = 'Post'
    post = Post.query.get_or_404(post_id)
    return render_template('single_post.html', title = title, post = post)


# @TODO: Update a Post
# @app.route('/single-post/<int:post_id>/comment', methods=['GET', 'POST'])
# @login_required
# def comment(post_id):
#     post = Post.query.get_or_404(post_id)
#     title = 'Comment'
#     form = Comment()
#     if form.validate_on_submit():
#         post.post_content = form.post_content.data
#         db.session.commit()
#         return redirect(url_for('single_post', post_id = post.id))
#     elif request.method == 'GET':
#         form.post_content.data = post.content

#     return render_template('post.html', title=title,legend='Comment', form = form)


@app.route('/single-post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Comment()
    if form.validate_on_submit():
        post.title = form.post_title.data
        post.content = form.post_content.data

        db.session.commit()
        return redirect(url_for('single_post', post_id=post.id))
    elif request.method == 'GET':  
        form.post_title.data = post.title
        form.post_content.data = post.content
    return render_template('post.html',legend='Update Post', form = form)


    
