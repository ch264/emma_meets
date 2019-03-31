import os, datetime
# from app import db, app
from peewee import *

# Peewee provides advanced support for SQLite and Postgres via database-specific extension modules.
from playhouse.postgres_ext import PostgresqlExtDatabase
db = PostgresqlExtDatabase('app', user='christinahastenrath', register_hstore=True)


# DATABASE = PostgresqlDatabase('emma', user='christinahastenrath')
DATABASE = SqliteDatabase('emma.db')


# initialise a database
# db = PostgresqlDatabase(
#     'database_name',  # Required by Peewee.
#     user='postgres',  # Will be passed directly to psycopg2.
#     password='secret',  # Ditto.
#     host='db.mysite.com')  # Ditto.

# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/appdb'
# psql postgres://USERNAME:PASSWORD@babar.elephantsql.com:5432/jszlmeae
# psql (9.3.4, server 9.2.8)
# SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)
# Type "help" for help.

# or pg_db = PostgresqlDatabase('my_app', user='postgres', password='secret',
#                            host='10.1.0.9', port=5432)

class User(Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)
	about_me = TextField()
	age = IntegerField()
	gender = CharField()
	location = TextField()
	fav_snack = CharField(255)
	fav_toy = CharField(255)
	breed = CharField()
	# image_filename = CharField()
	# image_url = CharField()

	class Meta:
		database = DATABASE
		db_table = 'user'

	@classmethod
	def create_user(cls, username, about_me, age, gender, location, fav_snack, fav_toy, breed, image_filename, image_url):
		try:
			cls.create(
				username = username,
				about_me = about_me,
				# age = age,
				gender = gender,
				location = location,
				fav_snack = fav_snack,
				fav_toy = fav_toy,
				breed = breed,
				# image_filename = image_filename,
				# image_url = image_url
			)
		except IntegrityError:
			raise ValueError('create error')

class Category(Model):
	name = CharField()

	class Meta:
		database = DATABASE
		db_table = 'category'

	@classmethod
	def create_category(cls, name):
		try:
			cls.create(
				name = name
			)
		except IntegrityError:
			raise ValueError("create category error")


class Product(Model):
	name = CharField()
	location = TextField()
	website = CharField()
	image_url = CharField()
	image_filename = CharField()
	category = ForeignKeyField(model=Category, backref='product_category')

	class Meta:
					database = DATABASE
					db_table = 'product'

	@classmethod
	def create_product(cls, name, location, website, image_url, image_filename, category):
		try:
			cls.create(
				name = name,
				location = location,
				website = website,
				image_url = image_url,
				image_filename = image_filename,
				category = category)
		except IntegrityError:
			raise ValueError('create product error')




class Review(Model):
	title = CharField()
	body = TextField()
	timestamp = DateTimeField(default=datetime.datetime.now())
	user = ForeignKeyField(model=User, backref="user_review")
	product = ForeignKeyField(model=Product, backref="product_review")
	rating = IntegerField()

	class Meta:
			database = DATABASE
			db_table = 'review'
	
	@classmethod
	def create_review(cls, title, body, user, product, rating):
		try:
			cls.create(
				title = title,
				body = body,
				user = user,
				product = product,
				rating = rating
			)
		except IntegrityError:
			raise ValueError("create review error")







def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Product, Review, Category], safe=True)
	DATABASE.close()
