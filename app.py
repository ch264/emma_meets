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
from flask_oauth import OAuth




# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '110906266153-gq3b4tr0daql4h79p4eh9nkegcff3831.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '4B7YUAggeupJC36DVbghtach'
REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console

SECRET_KEY = 'development key'
DEBUG = True



app = Flask(__name__)
# app.config.from_object(Config)
app.secret_key = 'pickle'
oauth = OAuth()

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# Sets variable images to uploader
# images = UploadSet('images', IMAGES)
# configure_uploads(app, images)



# @login_manager.user_loader
# def load_user(userid):
#     try: 
#         return models.User.get(models.User.id == userid)
#     except models.DoesNotExist:
#         return None






# Connects to database and gets current user who is logged in
@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()
  # g.user = current_user

# Closes connection to database after request finishes
@app.after_request
def after_request(response):
  g.db.close()
  return response




# ====================================================================
# =========================  Google Auth  =========================
# ====================================================================
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/signup')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib.request import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError or e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()

    return res.read()


@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)



@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')




# ====================================================================
# =========================  Initial Routes  =========================
# ====================================================================
		
@app.route('/')
def main():
	user = {'username': 'Miguel'}
	return render_template('landing.html', user=user)

@app.route('/about')
def about():
	return render_template('about.html')


# ====================================================================
# ========================  User Auth Routes  ========================
# ====================================================================





# @app.route('/signup', methods=('GET', 'POST'))
# def register():
#     # Access SignUpForm from forms.py
#     form = forms.SignUpForm()

#     if form.validate_on_submit():
#         # Sets variable filename to image file of uploaded 'profile_image' from form
#         # filename = images.save(request.files['profile_image'])
#         # Sets variable url to change image url to match filename
#         # url = images.url(filename)
#         # Calls method 'create_user' as defined in models.py to create a user in database
#         models.User.create_user(
#             username=form.username.data,
#             # email=form.email.data,
#             # password=form.password.data,
# 						about_me=form.about_me.data,
# 						# age = form.age.data,
# 						location = form.location.data,
# 						fav_snack = form.fav_snack.data,
# 						fav_toy = form.fav_toy.data,
# 						breed = form.breed.data,
# 						gender = form.gender.data)
#             # image_filename=filename,
#             # image_url=url)
        
#         # Gets newly created user from the database by matching username in the database to username entered in the form
#         user = models.User.get(models.User.username == form.username.data)
#         # Creates logged in session
#         login_user(user)
#         flash('Thank you for signing up', 'success')
#         # Pass in current/logged in user as parameter to method 'profile' in order to redirect user to profile after signing up
#         return redirect(url_for('profile', username=user.username))

#     # Initial visit to this page renders the Sign Up template with the SignUpForm passed into it
#     return render_template('signup.html', form=form)



# # Route and method to login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Access LoginForm from forms.py
#     form = forms.LoginForm()

#     if form.validate_on_submit():
#         try:
#             # Find user using email address
#             user = models.User.get(models.User.email == form.email.data)
#         except models.DoesNotExist:
#             flash("Email or password not found.  Please sign up!", "error")
#         else:
#             # Check hashed password in database against user's typed password
#             if check_password_hash(user.password, form.password.data):
#                 # Creates logged in session
#                 login_user(user)
#                 flash("You successfully logged in", "success")

#                 # Upon successful login, redirect to user's profile page with user passed in as a parameter to the method 'profile'
#                 return redirect(url_for('profile', username=user.username))
#             else:
#                 # If passwords don't match, flash error message
#                 flash("Your email or password doesn't match", "error")
    
#     # Initial visit to this page renders the login template with the LoginForm passed into it
#     return render_template('login.html', form=form)

# # Route and method to logout
# @app.route('/logout')
# @login_required
# def logout():
#     # Ends logged in session
#     logout_user()
#     # Redirects user to 'index' method for landing page
#     return redirect(url_for('index'))


# ====================================================================
# =========================  Profile Routes  =========================
# ====================================================================
# Route and method to go to a user's profile
@app.route('/profile')
def profile():
	return render_template('profile.html', user=user)


# @app.route('/login')



if __name__ == '__main__':
	models.initialize()
	# try:
	# 	models.Category.create_category(
	# 		name='name')
	# 		except ValueError:
	# 			pass


PORT = 5000
DEBUG = True

# app.config['DEBUG'] = True
app.run(port=PORT, debug=DEBUG)


