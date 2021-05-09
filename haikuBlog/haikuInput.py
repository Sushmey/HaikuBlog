from flask import session
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
import syllapy
from haikuBlog import mysql


def validate_haiku(form,haiku):
	words = haiku.data.split()
	syllables = 0
	for word in words:
		word = word.lower()
		syllables+=syllapy.count(word)
	if (syllables != 17):
		raise ValidationError("Check the number of syllables")		


class Haiku(FlaskForm):
	haiku = StringField('Haiku',validators=[InputRequired(), validate_haiku])
	title = StringField('Title',validators=[InputRequired(),Length(max=140)])
	submit = SubmitField('Post!')

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[InputRequired(),Length(min=3,max=20)])
	email = StringField('Email', validators=[InputRequired(),Email()])
	password = PasswordField('Password', validators=[InputRequired(),Length(min=6)])
	confirmPassword = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('password')])
	submit = SubmitField('Register!')

	def validate_username(self, username):
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM User WHERE username='{username}'".format(username=username.data))
		user = cursor.fetchall()
		if user:
			raise ValidationError("Username is taken")	
	def validate_email(self, email):
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM User WHERE email='{email}'".format(email=email.data))
		emailID = cursor.fetchall()
		cursor.close()
		if emailID:
			raise ValidationError("Account already exists with that email")		

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[InputRequired(),Email()])
	#username = StringField('Username',validators=[InputRequired(),Length(min=3,max=20)])
	password = PasswordField('Password', validators=[InputRequired(),Length(min=6)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login!')

	def validate_email(self, email):
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM User WHERE email='{email}'".format(email=email.data))
		emailID = cursor.fetchall()
		cursor.close()
		if (emailID==()):
			raise ValidationError("Account does not exist. Please sign up")			

class ProfileUpdateForm(FlaskForm):
	username = StringField('Username',validators=[InputRequired(),Length(min=3,max=20)])
	email = StringField('Email', validators=[InputRequired(),Email()])
	pfp = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update!')

	def validate_username(self, username):
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM User WHERE username='{username}'".format(username=username.data))
		user = cursor.fetchall()
		cursor.execute("SELECT * FROM User WHERE user_id='{user_id}'".format(user_id=session['user_id']))
		userDetails = cursor.fetchall()
		cursor.close()
		if user and userDetails[0]['username']!=username.data:
			raise ValidationError("Username is taken")	
	def validate_email(self, email):
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM User WHERE email='{email}'".format(email=email.data))
		emailID = cursor.fetchall()
		cursor.execute("SELECT * FROM User WHERE user_id='{user_id}'".format(user_id=session['user_id']))
		userDetails = cursor.fetchall()
		cursor.close()
		if emailID and userDetails[0]['email']!=email.data:
			raise ValidationError("Account already exists with that email")	




