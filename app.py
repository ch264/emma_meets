import os
from flask import Flask, g, request, render_template, flash, redirect, url_for, session, escape
# from config import Config

# User login
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import check_password_hash
import models, forms
# Image uploader
# from flask_uploads import UploadSet, configure_uploads, IMAGES

# Google Oauth
# from flask_oauth import OAuth

# import functools
# import flask
# from authlib.client import OAuth2Session
# import google.oauth2.credentials
# import googleapiclient.discovery

# ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
# AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

# AUTHORIZATION_SCOPE ='openid email profile'

# AUTH_REDIRECT_URI = os.environ.get("FN_AUTH_REDIRECT_URI", default=False)
# BASE_URI = os.environ.get("FN_BASE_URI", default=False)
# CLIENT_ID = os.environ.get("FN_CLIENT_ID", default=False)
# CLIENT_SECRET = os.environ.get("FN_CLIENT_SECRET", default=False)

# AUTH_TOKEN_KEY = 'auth_token'
# AUTH_STATE_KEY = 'auth_state'
# USER_INFO_KEY = 'user_info'





# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
# GOOGLE_CLIENT_ID = '110906266153-gq3b4tr0daql4h79p4eh9nkegcff3831.apps.googleusercontent.com'
# GOOGLE_CLIENT_SECRET = '4B7YUAggeupJC36DVbghtach'
# REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console

# SECRET_KEY = 'development key'
# DEBUG = True



app = Flask(__name__)
# app.config.from_object(Config)
app.secret_key = 'pafajeihguihawiorhgl'
# app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

# oauth = OAuth()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sets variable images to uploader
# images = UploadSet('images', IMAGES)
# configure_uploads(app, images)



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
# =========================  Google Auth  =========================
# ====================================================================
# google = oauth.remote_app('google',
#                           base_url='https://www.google.com/accounts/',
#                           authorize_url='https://accounts.google.com/o/oauth2/auth',
#                           request_token_url=None,
#                           request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
#                                                 'response_type': 'code'},
#                           access_token_url='https://accounts.google.com/o/oauth2/token',
#                           access_token_method='POST',
#                           access_token_params={'grant_type': 'authorization_code'},
#                           consumer_key=GOOGLE_CLIENT_ID,
#                           consumer_secret=GOOGLE_CLIENT_SECRET)

# @app.route('/signup')
# def index():
#     access_token = session.get('access_token')
#     if access_token is None:
#         return redirect(url_for('login'))

#     access_token = access_token[0]
#     from urllib.request import Request, urlopen, URLError

#     headers = {'Authorization': 'OAuth '+access_token}
#     req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
#                   None, headers)
#     try:
#         res = urlopen(req)
#     except URLError or e:
#         if e.code == 401:
#             # Unauthorized - bad token
#             session.pop('access_token', None)
#             return redirect(url_for('login'))
#         return res.read()

#     return res.read()


# @app.route('/login')
# def login():
#     callback=url_for('authorized', _external=True)
#     return google.authorize(callback=callback)



# @app.route(REDIRECT_URI)
# @google.authorized_handler
# def authorized(resp):
#     access_token = resp['access_token']
#     session['access_token'] = access_token, ''
#     return redirect(url_for('index'))


# @google.tokengetter
# def get_access_token():
#     return session.get('access_token')



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
# ========================  User Auth Routes  ========================
# ====================================================================

# @app.route('/')
# def index():
#     if is_logged_in():
#         user_info = get_user_info()
#         return 'You are currently logged in as ' + user_info['given_name']

#     return 'You are not currently logged in'

# def no_cache(view):
#     @functools.wraps(view)
#     def no_cache_impl(*args, **kwargs):
#         response = flask.make_response(view(*args, **kwargs))
#         response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
#         response.headers['Pragma'] = 'no-cache'
#         response.headers['Expires'] = '-1'
#         return response

#     return functools.update_wrapper(no_cache_impl, view)

# @app.route('/google/login')
# @no_cache
# def login():
#     session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=AUTHORIZATION_SCOPE, redirect_uri=AUTH_REDIRECT_URI)
#     uri, state = session.authorization_url(AUTHORIZATION_URL)
#     flask.session[AUTH_STATE_KEY] = state
#     flask.session.permanent = True
#     return flask.redirect(uri, code=302)


# @app.route('/google/auth')
# @no_cache
# def google_auth_redirect():
#     state = flask.request.args.get('state', default=None, type=None)
    
#     session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=AUTHORIZATION_SCOPE, state=state, redirect_uri=AUTH_REDIRECT_URI)
#     oauth2_tokens = session.fetch_access_token(ACCESS_TOKEN_URI, authorization_response=flask.request.url)
#     flask.session[AUTH_TOKEN_KEY] = oauth2_tokens

#     return flask.redirect(BASE_URI, code=302)

# @app.route('/google/logout')
# @no_cache
# def logout():
#     flask.session.pop(AUTH_TOKEN_KEY, None)
#     flask.session.pop(AUTH_STATE_KEY, None)
#     flask.session.pop(USER_INFO_KEY, None)

#     return flask.redirect(BASE_URI, code=302)

# def is_logged_in():
#     return True if AUTH_TOKEN_KEY in flask.session else False

# def build_credentials():
#     if not is_logged_in():
#         raise Exception('User must be logged in')

#     oauth2_tokens = flask.session[AUTH_TOKEN_KEY]
#     return google.oauth2.credentials.Credentials(
#         oauth2_tokens['access_token'],
#         refresh_token=oauth2_tokens['refresh_token'],
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         token_uri=ACCESS_TOKEN_URI)

# def get_user_info():
#     credentials = build_credentials()
#     oauth2_client = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
#     return oauth2_client.userinfo().get().execute()


# Flask sinup

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Access SignUpForm from forms.py
    form = forms.SignUpForm()

    if form.validate_on_submit():
        # Sets variable filename to image file of uploaded 'profile_image' from form
        # filename = images.save(request.files['profile_image'])
        # Sets variable url to change image url to match filename
        # url = images.url(filename)
        # Calls method 'create_user' as defined in models.py to create a user in database
			# print(form.username.data)
      models.User.create_user(
      	username=form.username.data,
        email=form.email.data,
        password=form.password.data,
				about_me=form.about_me.data,
						# age = form.age.data,
				gender = form.gender.data,
				location = form.location.data,
				fav_snack = form.fav_snack.data,
				fav_toy = form.fav_toy.data,
				breed = form.breed.data
				)
            # image_filename=filename,
            # image_url=url)
        
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
@app.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username=None):
  if username != None:
    # Finds user in database by username passed into URL
    user = models.User.select().where(models.User.username==username).get()
    # Finds all reviews in database where the user id stored with a reciew matches the found user aboves id
    reviews = models.Review.select().where(models.Review.user == user.id).order_by(models.Review.timestamp)
# finds all favorited products

    return render_template('profile.html', user=user, reviews=reviews)

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
    # user.password=form.password.data,
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

@app.route('/product', methods=['GET'])
@app.route('/product/<product_id>', methods=['GET'])
# @login_required
def product(product_id=None):
  # if product_id is provided as a paramter
  if product_id != None:
    # find single product in database using that id number
    product = models.Product.select().where(Product.id == product_id).get()
    # pass the found product to the individual product template
    return render_template('product.html', product=product)
  # if no product_is is provided as a parameter, select all product form the product table, limit 15 results
  products = models.Product.select().limit(20)
  # pass those products to the products template
  return render_template('products.html', products=products)

@app.route('/create-product', methods=['GET', 'POST'])
# @login_required
def add_product():
  # Access the ProductForm from forms.py
  form = forms.ProductForm()
  # Set variable user to current logged in user
  user = g.user._get_current_object()

  if request.method == 'POST':
    # Call method create_product defined in models.py for the Product model
    models.Product.create_product(
      name = form.name.data,
      location = form.location.data,
      website = form.website.data,
      category = form.category.data)
      # image_filename = filename,
      # image_url = url
    
    # Find new created product in database
    product = models.Product.get(models.Product == form.name.data)
    flash('Product Created', 'Success')
    # Redirect user to individual product page with found products id passed as parameter
    return redirect(url_for('product', product_id=product.id))
  # Render the create-product template with the ProductForm
  # Pass in the current_user in order to redirect user back to their profile if they choose to cancel create a product
  return render_template('create-product.html', form=form, user=user)

@app.route('/create-category', methods=['GET', 'POST'])
def add_category():
  form = forms.CategoryForm()
  user =g.user._get_current_object()
  if request.method == 'POST':
    models.Category.create_category(
      name = form.name.data
    )
    category = models.Category.get(models.Category == form.name.data)
    flash('Category created', 'Success')
    return redirect(url_for('product', product_id=product.id))
  return render_template('create-product.html', form=form, user=user)





PORT = 5000
DEBUG = True



@app.route('/products')
def products():
	return render_template('products.html')


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
  


