import os, datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
# from app import db, app
from peewee import *

# Peewee provides advanced support for SQLite and Postgres via database-specific extension modules.
# from playhouse.postgres_ext import PostgresqlExtDatabase
# db = PostgresqlExtDatabase('app', user='christinahastenrath', register_hstore=True)


DATABASE = SqliteDatabase('emma.db')
# DATABASE = PostgresqlDatabase('emma', user='christinahastenrath', password='secret', host='127.0.0.1', port=5432)

# initialise a database
# db = PostgresqlDatabase(
#     'database_name',  # Required by Peewee.
#     user='postgres',  # Will be passed directly to psycopg2.
#     password='secret',  # Ditto.
#     host='db.mysite.com')  # Ditto.
# or pg_db = PostgresqlDatabase('my_app', user='postgres', password='secret', host='10.1.0.9', port=5432)

# ====================================================================
# =========================  User Model  =============================
# ====================================================================

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)
	about_me = TextField()
	# age = IntegerField()
	gender = CharField()
	location = TextField()
	fav_snack = CharField(255)
	fav_toy = CharField(255)
	breed = CharField()
	image_filename = CharField()
	image_url = CharField()
        
	class Meta:
		database = DATABASE
		db_table = 'user'

	@classmethod
	def create_user(cls, username, email, password, about_me, gender, location, fav_snack, fav_toy, breed, image_filename, image_url):
		try:
			cls.create(
				username = username,
				email = email,
				password = generate_password_hash(password),
				about_me = about_me,
				# age = age,
				gender = gender,
				location = location,
				fav_snack = fav_snack,
				fav_toy = fav_toy,
				breed = breed,
				image_filename = image_filename,
				image_url = image_url)
		except IntegrityError:
			raise ValueError('create user error')
	
	# example, "give me all the users this user is following":
	def following(self):
		# query other users through the "relationship" table
		return (User
						.select()
						.join(Follow, on=Follow.to_user)
						.where(Follow.from_user == self)
						.order_by(User.username))

	def followers(self):
		return (User
						.select()
						.join(Follow, on=Follow.from_user)
						.where(Follow.to_user == self)
						.order_by(User.username))

	def is_following(self, user):
		return (Follow
						.select()
						.where(
								(Follow.from_user == self) &
								(Follow.to_user == user))
						.exists())


# ====================================================================
# ========================= Follow Model  ============================
# ====================================================================

class Follow(Model):
	follower = ForeignKeyField(User, backref="user_follower")
	followed = ForeignKeyField(User, backref="user_followed")
	class Meta:
		database = DATABASE
		db_table = 'follow'
		# indexes = (
    #         # Specify a unique multi-column index on follower/followed.
    #         (('follower', 'followed'), True),
    #     )

	def follower(self):
		User.select().join(Follow, on=Follow.followed).where(Follow.follower == user.id)
		for follower in Follow:
			print(follower)

	def following(self): 
		User.select().join(Follow, on=Follow.follower).where(Follower.followed == user.id)
		for followed in Follow:
			print(followed)

# 		# =================== 

# 	def follow(self, user):
# 		if not self.is_following(user):
# 			self.followed.append(user)

# 	def unfollow(self, user):
# 		if self.is_following(user):
# 			self.followed.remove(user)

# 	def is_following(self, user):
# 		return self.followed.filter(
# 			followers.c.followed_id == user.id).count() > 0


# ====================================================================
# =========================  Category Model  =========================
# ====================================================================
class Category(Model):
	name = CharField(unique=True)

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
			raise 
		

# ====================================================================
# =========================  Product Model  =========================
# ====================================================================
class Product(Model):
	name = CharField()
	location = TextField()
	website = CharField(unique=True)
	image_url = CharField()
	image_filename = CharField()
	category = ForeignKeyField(model=Category, backref='product_category')
	avg_rating = FloatField(default=None, null=True)
	class Meta:
					database = DATABASE
					db_table = 'product'

	@classmethod
	def create_product(cls, name, location, website, image_filename, image_url, category):
		try:
			cls.create(
				name = name,
				location = location,
				website = website,
				image_url = image_url,
				image_filename = image_filename,
				category = category
				)
		except IntegrityError:
			raise

	# get all categories and put them into a dictionary object. Convert Peewee select objcet to dictionary object. https://github.com/coleifer/peewee/issues/134
	@classmethod
	def get_categories(cls):
		query = Category.select()
		cursor = DATABASE.execute(query)
		
		ncols = len(cursor.description)
		colnames = [cursor.description[i][0] for i in range(ncols)]
		results = []

		for row in cursor.fetchall():
			res = {}
			for i in range(ncols):
				res[colnames[i]] = row[i]
			results.append(res)
		
		return results


	def average_rating(self):
		query = Review.select().where(Review.product_id == self.id)
		review_list = []
		for review in query:
			review_list.append(review.rating)
			print(review.rating)
		# print(sum(review_list) / len(review_list))
		if len(review_list) == 0: 
			return 0
		self.avg_rating = sum(review_list) / len(review_list)
		# return sum(review_list) / len(review_list)
		# self.avg_rating.save()
		self.save()
		# print(self, self.avg_rating)
		return self.avg_rating
		
# ====================================================================
# =========================  Review Model  ===========================
# ====================================================================
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
	def create_review(cls, title, user, product, rating, body):
		try:
			cls.create(
				title = title,
				body = body,
				user = user,
				product = product,
				rating = rating
			)
		except IntegrityError:
			raise 

	
class Saved(Model):
	# Sets user column to expect a foreign key (product Id)
	user = ForeignKeyField(User, backref='favorites')
	product = ForeignKeyField(Product, backref="favorites")
	timestamp = DateTimeField(default=datetime.datetime.now())

	class Meta:
		database = DATABASE
		db_table = 'saved'



# Defines initialize function to connect to database, create empty tables, and close connection
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Product, Review, Category, Saved, Follow], safe=True)
	DATABASE.close()
