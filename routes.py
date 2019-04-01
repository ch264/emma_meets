# from app import app
import models, app, forms, os

from flask import render_template, flash, redirect, url_for, Flask, g, request
from flask import Flask, g, request, render_template, flash, redirect, url_for, session, escape
# from config import Config

# User login
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import check_password_hash


# # Connects to database and gets current user who is logged in
# @app.before_request
# def before_request():
#   g.db = models.DATABASE
#   g.db.connect()
#   g.user = current_user

# # Closes connection to database after request finishes
# @app.after_request
# def after_request(response):
#   g.db.close()
#   return response



# ====================================================================
# =========================  Initial Routes  =========================
# ====================================================================
		

# @app.route('/', methods=['GET'])
# def index():
# 	return render_template('landing.html')


# @app.route('/about')
# def about():
# 	return render_template('about.html')



# ====================================================================
# ========================  User Auth Routes  ========================
# ====================================================================


# ====================================================================
# =========================  Profile Routes  =========================
# ====================================================================

# ====================================================================
# ==========================  Review Routes  =========================
# ====================================================================

# ====================================================================
# ================ Favorite products Routes  =========================
# ====================================================================


# if __name__ == '__main__':
# 	models.initialize()
# 	# try:
# 	# 	models.Category.create_category(
# 	# 		name='name')
# 	# 		except ValueError:
# 	# 			pass


# PORT = 5000
# DEBUG = True

# # app.config['DEBUG'] = True
# app.run(port=PORT, debug=DEBUG)

