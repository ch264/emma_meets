# from app import app
from app.models import User, Review, Category, Product
from app import app, db

from flask import render_template, flash, redirect, url_for, Flask, g, request


import os
import forms

@app.before_request
def before_request():
        db.session.commit()

@app.route('/')
def index():
	return 'Hello World! this is emma meets'



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
	return render_template('landing.html')

@app.route('/about')
def about():
	return render_template('about.html')

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