import os
from flask import Flask, g, request, render_template, flash, redirect, url_for, session, escape
# from config import Config

# User login
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import check_password_hash
import models, forms
# Redirect user when not logged in
from werkzeug.urls import url_parse


# Image uploader
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')
app.secret_key = 'pafajeihguihawiorhgl'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# ====================================================================
# =========================  Initial Routes  =========================
# ====================================================================
		# copied to routes
@app.route('/')
def index():
	return render_template('landing.html')

@app.route('/about')
def about():
	return render_template('about.html')


# ====================================================================
# ========================= User Auth Routes  =========================
# ====================================================================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Access SignUpForm from forms.py
    form = forms.SignUpForm()

    if form.validate_on_submit():
      # Sets variable filename to image file of uploaded 'profile_image' from form
      filename = images.save(request.files['profile_image'])
      # Sets variable url to change image url to match filename
      url = images.url(filename)
      # Calls method 'create_user' as defined in models.py to create a user in database
			# print(form.username.data)
      models.User.create_user(
        username = form.username.data,
        email = form.email.data,
        password = form.password.data,
				about_me=form.about_me.data,
						# age = form.age.data,
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

    # Initial visit to this page renders the Sign Up template with the SignUpForm passed into it
    return render_template('signup.html', form=form)

# Route and method to login
@app.route('/login', methods=['GET', 'POST'])
def login():
  # Access LoginForm from forms.py
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
    # Redirects user to 'index' method for landing page
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

    # finds all favorited products
    # Owner = user.alias()

    # saved_product = models.Saved.select(models.User, models.Product).join(models.Saved, on=models.Saved.product).where(models.User.username == current_user.userame)

    # query = models.Product.select().join(models.User).where(User.username == current_user)
    # print(current_user)
  
    # saved_product = (models.Saved.select(models.Saved, models.Product.name, models.Product.id, models.User.username)
    # .join(models.Saved)
    # .join(models.Product) 
    # .join(models.User))
    # ////////////////////////////////////////////
    # Owner = user.alias()
    # saved_product = (models.Saved.select(models.Saved, models.Product.name, models.Product.avg_rating, models.Product.website,models.Product.id, models.Product.image_filename, Owner.username)
    # .join(Owner) 
    # # .join(models.User)
    # .switch(models.Saved)
    # .join(models.Product))
    # # .join(models.User))
    # /////////////////////////////////////////////////
    saved_product = models.Saved.select(models.Saved, models.User, models.Product).join(models.User).switch(models.Saved).join(models.Product)
    return render_template('profile.html', user=user, reviews=reviews, saved_product=saved_product)
  return redirect(url_for('index'))


@app.route('/edit-profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username=None):
  # Finds user in database by logged in current user's id
  user = models.User.get(g.user.id)
  # Accesses EditUserForm from forms.py
  form = forms.EditUserForm()

  if form.validate_on_submit():
    # Set user's info in database to new values entered in form
    user.username = form.username.data
    user.email = form.email.data
    # user.password = form.password.data,
    user.about_me = form.about_me.data
        # age = form.age.data,
    user.gender = form.gender.data
    user.location = form.location.data
    user.fav_snack = form.fav_snack.data
    user.fav_toy = form.fav_toy.data
    user.breed = form.breed.data
    
    # Save changes to user in database
    user.save()
    flash('Your changes have been saved.', 'success')
    # Redirect to user's profile to reflect changes
    return redirect(url_for('profile', username=user.username))
  # set the breed field in the edit profile form to show the users breed
  form.breed.default = user.breed
  # processes the form with the category populated
  form.process()
  # Upon initial visit to route, serves up edit profile form
  return render_template('edit-profile.html', form=form, user=user)


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
# @login_required
def add_product():
  # Access the ProductForm from forms.py
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

  # Set variable user to current logged in user
  user = g.user._get_current_object()
 
  if form.validate_on_submit():
    # Sets variable filename to image file of uploaded 'product_image' from form
    filename = images.save(request.files['product_image'])
    # Sets variable url to change image url to match filename
    url = images.url(filename)
    # Call method create_product defined in models.py for the Product model
    prod = models.Product.create_product(
      name = form.name.data,
      location = form.location.data,
      website = form.website.data,
      category = form.category.data,
      image_filename = filename,
      image_url = url)
    product = models.Product.get(models.Product.website == form.website.data)
    print(product)
    # return render_template('create-product.html', form=form, user=user)
    # Find new created product in database
    
    flash('Product Created', 'Success')
    # Redirect user to individual product page with found products id passed as parameter
    return redirect(url_for('product', product_id=product.id))
  # Render the create-product template with the ProductForm
  # Pass in the current_user in order to redirect user back to their profile if they choose to cancel create a product
  
  # print(categories)
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
  if review_id != None:
    deleted_review = models.Review.delete().where(models.Review.id == review_id)
    deleted_review.execute()
    return redirect(url_for('profile'))
  return redirect(url_for('profile'))


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
    return render_template('edit-review.html', review=review, form=form)


# ====================================================================
# ========================= Saved Routes  =========================
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



PORT = 5000
DEBUG = True





# copied to routes

if __name__ == '__main__':
	models.initialize()

app.run(port=PORT, debug=DEBUG)
	# try:
	# 	models.Category.create_category(
	# 		name='name')
	# 		except ValueError:
	# 			pass

  # app.config['DEBUG'] = True
  


