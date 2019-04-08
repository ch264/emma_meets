import os
from flask import Flask, g, request, render_template, flash, redirect, url_for, session, escape
# from config import Config

# User login
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import check_password_hash, Bcrypt, generate_password_hash
import models, forms
# Redirect user when not logged in
from werkzeug.urls import url_parse

# email confirmation
from itsdangerous import URLSafeTimedSerializer
# ts = URLSafeTimedSerializer(app.secret_key)
from flask_mail import Mail, Message

# Image uploader
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')
app.secret_key = 'pafajeihguihawiorhgl'
# config for email sending
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lalatestingemma@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mysanfran3'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

bcrypt = Bcrypt(app)

# intialise extension
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# ts = URLSafeTimedSerializer(app.secret_key)

# Sets variable images to uploader
images = UploadSet('images', IMAGES)
configure_uploads(app, images)





@login_manager.user_loader
def load_user(userid):
  try: 
    return models.User.get(models.User.id == userid)
  except models.DoesNotExist:
    return None


# copies to routes
# Connects to database and gets current user who is logged in
@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()
  g.user = current_user

# Closes connection to database after request finishes
@app.after_request
def after_request(response):
  g.db.close()
  return response




# ====================================================================
# =========================  Error handlers  =========================
# ====================================================================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_error(error):
#     g.db.session.rollback()
#     return render_template('500.html'), 500


# ====================================================================
# =========================  Initial Routes  =========================
# ====================================================================
		# copied to routes
@app.route('/')
def index():
  def send_reset_email(user):
    token = user.get_reset_token()
    # msg = Message('Hello', sender = 'lalatestingemma@gmail.com', recipients = ['id1@gmail.com'])
    # msg.body = "This is the email body"
    # mail.send(msg)
    # return "Sent"
    msg = Message('Password Reset Request', sender='lalatestingemma@gmail.com', recipients =[user.email])
    msg.body = f''' 
    
    To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)} 
    
    If you did not make this request then simply ignore this email'''
    mail.send(msg)
    return "Sent"
  return render_template('landing.html')

@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/contact-us')
def contact_us():
	return render_template('contact-us.html')


# ====================================================================
# ========================= User Auth Routes  =========================
# ====================================================================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    print('out if create signup')
    print(request.form)
    if form.validate_on_submit():
      # Sets variable filename to image file of uploaded 'profile_image' from form
      filename = images.save(request.files['profile_image'])
      # Sets variable url to change image url to match filename
      url = images.url(filename)
      # Calls method 'create_user' as defined in models.py to create a user in database
      print('in if create user')
      models.User.create_user(
        username = form.username.data,
        email = form.email.data,
        password = form.password.data,
				about_me=form.about_me.data,
				age = form.age.data,
				gender = form.gender.data,
				location = form.location.data,
				fav_snack = form.fav_snack.data,
				fav_toy = form.fav_toy.data,
				breed = form.breed.data,
        image_filename=filename,
        image_url=url)
        
      # Gets newly created user from the database by matching username in the database to username entered in the form
      user = models.User.get(models.User.username == form.username.data)
        # Creates logged in session
      login_user(user)
      flash('Thank you for signing up', 'success')
        # Pass in current/logged in user as parameter to method 'profile' in order to redirect user to profile after signing up
      return redirect(url_for('profile', username=user.username))
    return render_template('signup.html', form=form)

# Route and method to login
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = forms.LoginForm()
  if form.validate_on_submit():
    try:
      # Find user using email address
      user = models.User.get(models.User.email == form.email.data)
    except models.DoesNotExist:
      flash("Email or password not found.  Please sign up!", "error")
    else:
      # Check hashed password in database against user's typed password
      if check_password_hash(user.password, form.password.data):
        # Creates logged in session
        login_user(user)
        flash("You successfully logged in", "success")
        # Upon successful login, redirect to user's profile page with user passed in as a parameter to the method 'profile'
        return redirect(url_for('profile', username=user.username))
      else:
        # If passwords don't match, flash error message
        flash("Your email or password doesn't match", "error")
  # Initial visit to this page renders the login template with the LoginForm passed into it
  return render_template('login.html', form=form)

# Route and method to logout
@app.route('/logout')
@login_required
def logout():
  # Ends logged in session
  logout_user()
  return redirect(url_for('index'))


# ====================================================================
# =========================  Profile Routes  =========================
# ====================================================================
# Route and method to go to a user's profile
@app.route('/profile/<username>', methods=['GET', 'DELETE'])
@login_required
def profile(username=None):
  if username != None:
    # Finds user in database by username passed into URL
    user = models.User.select().where(models.User.username==username).get()
    # Finds all reviews in database where the user id stored with a reciew matches the found user aboves id
    reviews = models.Review.select().where(models.Review.user == user.id).order_by(-models.Review.timestamp)
    
    saved_product = models.Saved.select(models.Saved, models.User, models.Product).join(models.User).switch(models.Saved).join(models.Product)

    # //////////////treehouse ///////////
    # finds all followers and followed
    # following = models.Follow.select().where(models.Follow)


    return render_template('profile.html', user=user, reviews=reviews, saved_product=saved_product)
  return redirect(url_for('index'))

def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request', sender='lalatestingemma@gmail.com', recipients =[user.email])
  msg.body = f''' To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)} If you did not make this request then simply ignore this email'''
  mail.send(msg)
  return "Sent"



@app.route('/edit-profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username=None):
  user = models.User.get(g.user.id)
  form = forms.EditUserForm()

  if form.validate_on_submit():
    user.username = form.username.data
    user.email = form.email.data
    # user.password = generate_password_hash(form.password.data)
    # user.password = form.password.data
    user.about_me = form.about_me.data
    user.age = form.age.data
    user.gender = form.gender.data
    user.location = form.location.data
    user.fav_snack = form.fav_snack.data
    user.fav_toy = form.fav_toy.data
    user.breed = form.breed.data
    user.image_filename = form.image_filename.data
    
    user.save()
    flash('Your changes have been saved.', 'success')
    # Redirect to user's profile to reflect changes
    return redirect(url_for('profile', username=user.username))
  # # set the breed field in the edit profile form to show the users breed
  # form.breed.default = user.breed
  # # processes the form with the category populated
  # form.process()
  return render_template('edit-profile.html', form=form, user=user)

# ====================================================================
# =========================  Follow Routes  =========================
# ====================================================================

# //////////////// MegaFlask Tutorial //////////////////

@app.route('/follow/<username>')
@login_required
def follow(username):
  user = User.query.filter_by(username=username).first()
  if user is None:
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot follow yourself!')
    return redirect(url_for('profile', username=username))
  current_user.follow(user)
  flash('You are following {}!'.format(username))
  return redirect(url_for('profile', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
  user = User.query.filter_by(username=username).first()
  if user is None:
    flash('User {} not found.'.format(username))
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot unfollow yourself!')
    return redirect(url_for('user', username=username))
  current_user.unfollow(user)
  db.session.commit()
  flash('You are not following {}.'.format(username))
  return redirect(url_for('user', username=username))

# //////////////// Treehouse tutorial ////////////////////////////
# @app.route('/follow/<username>')
# @login_required
# def follow(username):
#   try:
#     user = models.User.get(models.User.username == current_user.username)
#     models.Follow.create(
#         follower = g.user._get_current_object(),
#         followed = user
#     )
#   except models.DoesNotExist:
#     pass
#   return redirect(url_for('index'))

# @app.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
#     try:
#       user = models.User.get(models.User.id == username)
      
#       models.Follow.get(
#         models.Follow.follower == g.user._get_current_object(),
#         models.Follow.followed == user
#       ).delete_instance()
#     except models.DoesNotExist:
#       pass
#     return render_template('profile.html', user=user.username)
  

# ====================================================================
# =========================  Product Routes  =========================
# ====================================================================

@app.route('/products', methods=['GET'])
def products(product_id=None):
  products = models.Product.select().where(models.Product.id == product_id)
  return render_template('products.html', products=products)

@app.route('/product', methods=['GET'])
@app.route('/product/<product_id>', methods=['GET'])
@login_required
def product(product_id=None):
  if product_id != None:
    product = models.Product.select().where(models.Product.id == product_id).get()
    reviews= models.Review.select().where(models.Review.product == product_id).order_by(-models.Review.timestamp)
    # call average rating function that calculates reviews average rating
    rating = product.average_rating()
    return render_template('product.html', product=product, reviews=reviews, rating=rating)
  # if no product_is is provided as a parameter, select all product form the product table, limit 15 results
  products = models.Product.select().limit(15)
  # pass those products to the products template
  return render_template('products.html', products=products)

@app.route('/create-product', methods=['GET', 'POST'])
@login_required
def add_product():
  form = forms.ProductForm()

  # choices accepts an array of tuples which is immtable.
  categories = models.Product.get_categories()
  if len(categories) > 0:
    choices = []
    for category in categories:
      # turn tuple into list temp
      temp = []
      for k,v in category.items():
        if(k=='id'):
          # append key value into list
          temp.append(str(v))
        else:
          temp.append(v)
      # turn list back into tuple and append back into the array choicese
      choices.append(tuple(temp))
    form.category.choices = choices

  user = g.user._get_current_object()

  if form.validate_on_submit():
    filename = images.save(request.files['product_image'])
    url = images.url(filename)

    prod = models.Product.create_product(
      name = form.name.data,
      location = form.location.data,
      website = form.website.data,
      category = form.category.data,
      image_filename = filename,
      image_url = url)
    product = models.Product.get(models.Product.website == form.website.data)
    
    # return render_template('create-product.html', form=form, user=user)
    # Find new created product in database
    
    flash('Product Created', 'Success')
    return redirect(url_for('product', product_id=product.id))
  return render_template('create-product.html', form=form, user=user, categories=categories)

@app.route('/create-category', methods=['GET', 'POST'])
def add_category():
  form = forms.CategoryForm()
  user = g.user._get_current_object()
  if form.validate_on_submit():
    cat = models.Category.create_category(
      name = form.name.data
    )
    category = models.Category.get(models.Category.name == form.name.data)
    flash('Category created', 'Success')
    return redirect(url_for('product'))
  return render_template('create-category.html', form=form, user=user)

@app.route('/edit-product/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id=None):
  form = forms.EditProductForm()
  user = g.user._get_current_object()
  product = models.Product.select().where(models.Product.id == product_id).get()
  if product_id != None:
    product = models.Product.select().where(models.Product.id == product_id).get()
    if form.validate_on_submit():
      product = models.Product.select().where(models.Product.id == product_id).get()
      product.name = form.name.data
      product.location = form.location.data
      product.website = form.website.data
      product.save()
      flash('Your edited Product is now online', 'success')
      return redirect(url_for('product', product_id=product.id))
    # form.process()
    return render_template('edit-product.html', product=product, form=form, user=user)
# ====================================================================
# =========================  Review Routes  =========================
# ====================================================================

@app.route('/review/<product_id>', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
  
  form = forms.ReviewForm()
  print('out if')
  print(request.form)
  product = models.Product.select().where(models.Product.id == product_id).get()
  if form.validate_on_submit():
    print(form.rating.data)
    models.Review.create_review(
      title = form.title.data,
      user = g.user._get_current_object(),
      product = product.id,
      rating = form.rating.data,
      body = form.body.data
    )
    review = models.Review.get(models.Review.title == form.title.data)
    flash('Review created!', 'Success')
    return redirect(url_for('product', product_id=product.id))
  return render_template('create-review.html', form=form, user=current_user, product=product)


@app.route('/delete-review/<review_id>', methods=['GET', 'DELETE'])
@login_required
def delete_review(review_id=None):
  user = g.user._get_current_object()
  if review_id != None:
    deleted_review = models.Review.delete().where(models.Review.id == review_id)
    deleted_review.execute()
    return redirect(url_for('profile', username=user.username))
  return redirect(url_for('profile', username=user.username))


@app.route('/edit-review/<review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id=None):
  form = forms.EditReviewForm()
  review = models.Review.select().where(models.Review.id == review_id).get()
  user = g.user._get_current_object()
  if review_id != None:
    review = models.Review.select().where(models.Review.id == review_id).get()
    if form.validate_on_submit():
      review = models.Review.select().where(models.Review.id == review_id).get()
      review.title = form.title.data
      review.body = form.body.data
      review.rating = form.rating.data
      review.save()
      flash('Your edited your review', 'success')
      return redirect(url_for('profile', username=user.username))
    form.process()
    return render_template('edit-review.html', review=review, form=form, product=product)

# ====================================================================
# ========================= Saved favorite Routes  =========================
# ====================================================================

# create route to add data to join table
@app.route('/save/<product_id>')
def save_to_profile(product_id=None):
  user = g.user._get_current_object()
  # user = models.User.get(g.user.id)
  product = models.Product.get(models.Product.id == product_id)
  print(user.id)
  models.Saved.create(
    user=user.id, 
    product=product_id)
  return redirect(url_for('profile', username=user.username))
  # return redirect(url_for('product'))


@app.route('/remove/<product_id>', methods=['GET', 'DELETE'])
@login_required
def remove_saved(product_id=None):
  # user = models.User.get(g.user.id)
  user = g.user._get_current_object()
  if product_id != None:
    remove_saved = models.Saved.delete().where(models.Saved.user == user.id and models.Saved.product == product_id)
    remove_saved.execute()
    return redirect(url_for('profile', username=user.username))
  return redirect(url_for('profile', username=user.username))


# ====================================================================
# ========================= Email Routes  =========================
# ====================================================================
# build reset password with help from Corey Schafer:
# https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/10-Password-Reset-Email/flaskblog

# request to reset password, shows form to input email address
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = forms.RequestResetForm()

  if form.validate_on_submit():
    print('in if')
    # user = models.User.query.filter_by(email=form.email.data).first()
    user = models.User.get(models.User.email == form.email.data)
    # if user:
    send_reset_email(user)
    flash('An email has been sent to reset password', 'info')
    return redirect(url_for('login'))
  return render_template('reset_request.html', title='Reset Password', form=form)


# reset password route
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  user = models.User.verify_reset_token(token)
  if not user:
    print('invalid token')
  # if user is None:
    # pass in class warningk, can be used by css
    flash('That is an invalid or expired token', 'warning')
    return redirect(url_for('reset_request'))
  form = forms.ResetPasswordForm()
  print('show form reset password')
  if form.validate_on_submit():
    print('in hashed password')
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user.password = hashed_password
    user.save()
    flash('Your password has been updated!, please log in')
    return redirect(url_for('login'))
  return render_template('reset_token.html', title='Reset Password',form=form)


# use salt when generating a token


# @app.route('/reset', methods=["GET", "POST"])
# def reset():
#   form = forms.EmailForm()
#   if form.validate_on_submit():
#     user = User.query.filter_by(email=form.email.data)
#     token = ts.dumps(self.email, salt='recover-key')

#     recover_url = url_for('reset_with _token', token=token, _external=True)

#     html = render_template('email-recover.html', recover_url=recover_url)
# # Let's assume that send_email was defined in myapp/util.py
#     send_email(user.email, subject, html)
#     return redirect(url_for('index'))
#   return render_template('reset.html', form=form)

# @app.route('/reset/<token>', methods=['GET', 'POST'])
# def reset_with_token(token):
#   try:
#     email = ts.loads(token, salt="recover-key", max_age=86400)
#   except:
#     abort(404)

#   form = PasswordForm()

#   if form.validate_on_submit():
#     user = User.query.filter_by(email=email).first_or_404()

#     user.password = form.password.data

#     db.session.add(user)
#     db.session.commit()

#     return redirect(url_for('signin'))

#   return render_template('reset_with_token.html', form=form, token=token)




# PORT = 5000
# DEBUG = True

# if on heroku initialise this:
if 'ON_HEROKU' in os.environ:
  print('hitting ')
  models.initialize()


if __name__ == '__main__':
	models.initialize()

# app.run(port=PORT, debug=DEBUG)
	# try:
	# 	models.Category.create_category(
	# 		name='name')
	# 		except ValueError:
	# 			pass

  # app.config['DEBUG'] = True
  


