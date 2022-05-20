from turtle import title
from flask import render_template,url_for,flash,redirect, request,abort
from flask_login import login_user,current_user, logout_user, login_required
from zebus import app,db,bcrypt
from zebus.forms import  RegistrationForm, LoginForm, PostForm


import json
import requests
from zebus.models import User, Post,Quote

from zebus.models import User,Post


def get_quote():
    url = 'http://quotes.stormconsultancy.co.uk/random.json'
    req = requests.get(url)
    data = req.json()
    quote = Quote(data['quote'],data['author'])
    return quote


@app.route('/')
@app.route('/about')
def about():
  quote = get_quote()
  print(quote)
  return render_template('about.html', title= 'About', quote=quote)



@app.route ('/home')
def home():
  posts=Post.query.all()
  return render_template ('home.html', posts=posts)








@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))

  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Your Account has been  created! You can login','success')
    return redirect(url_for('login'))


  
  return render_template ('register.html', title='Register', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user  = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else  redirect (url_for('home'))

    else:
      flash('Login unsuccesful, please check email and password', 'danger')

  return render_template('login.html', title= 'login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
  return render_template('account.html', title= 'Account')



@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post has been created successfully!', 'info')
    return redirect (url_for("home"))

  return render_template('create_post.html', title= 'New Post', form=form, legend='New Post')


@app.route('/post/<int:post_id>')
def post (post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
   post = Post.query.get_or_404(post_id)
   if post.author!= current_user:
     abort(403)
   form = PostForm()
   if form.validate_on_submit():
     post.title = form.title.data
     post.content = form.content.data
     db.session.commit()
     flash ('Your post has been updated successfully')
     return redirect(url_for('post', post_id=post.id))
   
   elif  request.method == 'GET':
     form.title.data = post.title
     form.content.data = post.content
   return render_template('create_post.html', title='Update post', form=form, legend='Update Post')





