import os
from flask import Flask, g, request, render_template, flash, redirect, url_for, session, escape
# from config import Config

import models

app = Flask(__name__)
# app.config.from_object(Config)
app.secret_key = 'pickle'



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
# =========================  Initial Routes  =========================
# ====================================================================
		
@app.route('/')
def index():
	user = {'username': 'Miguel'}
	return render_template('landing.html', user=user)

@app.route('/about')
def about():
	return render_template('about.html')


# ====================================================================
# ========================  User Auth Routes  ========================
# ====================================================================

# ====================================================================
# =========================  Profile Routes  =========================
# ====================================================================
# Route and method to go to a user's profile
@app.route('/profile')
def profile():
	return render_template('profile.html', user=user)




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


