from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, SubmitField, IntegerField, FileField, TextField
from wtforms.validators import DataRequired, Regexp, ValidationError, Length, EqualTo, Email

# Imports for file/photo uploader
# from flask_wtf.file import FileField, FileRequired, FileAllowed

# Imports User model
from models import User

# Defines function name_exists to check if user exists in database with same username
def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with this username already exists")

# Defines function email_exists to check is user exists in database with same email
def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with this email already exists")


# Creates a SignUpForm inheriting from Form from flask_wtf
class SignUpForm(Form):
    # Sets names of fields equal to what type of data to receive
		username = StringField(
			# Label for the field
			'Username',
			validators=[
				# Requires user to enter something
				DataRequired(),
				# Limits characters to alphanumeric
				Regexp(
					r'^[a-zA-Z0-9_]+$',
					message=("Username should be one word, letters, "
										"numbers, and underscores only.")),
				# Calls previously defined function
				name_exists
			])
		email = StringField(
			'Email',
			validators=[
				DataRequired(),
				Email(),
				email_exists
			])
		password = PasswordField(
			'Password',
			validators=[
				DataRequired(),
				Length(min=2),
				# Checks that user entered password correctly in both password fields
				EqualTo('password2', message='Passwords must match')
			])
		password2 = PasswordField(
			'Confirm Password',
			validators=[DataRequired()
			])
		location = StringField(
			'Location',
      validators=[
        DataRequired()
      ])
		about_me = StringField(
			'About Me', 
			validators=[
				DataRequired(),
				Length(min=2)
			])
			# convert to integerfield
		# age = StringField()(
		# 	'Age', 
		# 	)
		gender = SelectField(
			'Gender', 
			choices=[(
				'male', 'Male'), ('female', 'Female')
			])
		location = StringField(
			'Location', 
			validators=[DataRequired()
			])
		fav_snack = StringField(
			'Favorite Snack', 
			validators=[DataRequired()
			])
		fav_toy = StringField(
			'Favorite Toy', 
			validators=[DataRequired(
			)])
		breed = StringField(
			'Breed', 
			validators=[DataRequired()
			])
		# profile_image = FileField('Profile Image')


# Creates a LoginForm class. Do not need if use Google 
class LoginForm(Form):
		email = StringField(
			'Email',
			validators=[
				DataRequired(),
				Email()
			])
		password = PasswordField(
			'Password',
			validators=[DataRequired()]
			)
		remember_me = BooleanField('Remember Me')
		submit = SubmitField('Sign In')

# Creates an EditUserForm class
class EditUserForm(Form):
		# username =  StringField('Username', validators=[name_exists])
		username =  StringField('Username')
		email = StringField('Email')
		about_me = StringField('About Me', validators=[DataRequired()])
		# age = StringField()('Age', validators=DataRequired())
		gender = SelectField('Gender', choices=[('male', 'female')])
		location = StringField('Location', validators=[DataRequired()])
		fav_snack = StringField('Favorite Snack', validators=[DataRequired()])
		fav_toy = StringField('Favorite Toy', validators=[DataRequired()])
		breed = StringField('Breed', validators=[DataRequired()])
		# profile_image = FileField('Profile Image')

# Creates an EditRecipeForm class

class CategoryForm(Form):
	name = StringField(
		'Name',
		validators=[
			DataRequired(),
			Length(min=1, max=140)
		])
	submit = SubmitField('Submit')

# Create a new Product Form
class ProductForm(Form):
	name = TextField(
        'Name',
        validators=[
            DataRequired()
        ])
	location = TextField(
        'Location',
        validators=[
            DataRequired()
        ])
	website = TextField(
        'Website',
        validators=[
            DataRequired()
        ])
	# product_image = FileField('Profile Image')
	category = SelectField('Category', choices=[], validators=[DataRequired()])
	# submit = SubmitField('Submit')


	class EditProductForm(Form):
		name = StringField('name')
		location = StringField('Location')
		website = StringField('Website')
		product_image = FileField('Profile Image')
		category = SelectField('Category', choices=[], validators=[DataRequired()])

# Creates a new ReviewForm
class ReviewForm(Form): 
	
		rating = SelectField(
			'Rating', 
			choices=[('5', '5'),('4','4'), ('3','3'), ('2','2'), ('1','1')], 
			validators=[DataRequired()])
		title = TextField(
				'Title',
				validators=[DataRequired()])
		body = TextAreaField(
				'Let us konw what you think',
				validators=[DataRequired()]
				)
		submit = SubmitField('Submit')
		
			
		
  #  do we need ain image placeholder for the image of who is leaving the rview?

class EditReviewForm(Form):
    # Provides same category options as create review form
		title = StringField('Title')
		content = TextAreaField('Content')
		rating = SelectField(
			'Rating', 
			choices=[('5', '5'),('4','4'), ('3','3'), ('2','2'), ('1','1')
			])
 