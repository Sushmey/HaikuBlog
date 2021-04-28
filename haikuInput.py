from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
import syllapy


def validate_haiku(form,haiku):
	syllables2 = syllapy.count(haiku.data)
	words = haiku.data.split()
	syllables = 0
	for word in words:
		word = word.lower()
		syllables+=syllapy.count(word)
	if (syllables != 17 and syllables2 !=17):
		raise ValidationError("Check the number of syllables")		


class Haiku(FlaskForm):
	haiku = StringField('Haiku',validators=[InputRequired(), validate_haiku])

	submit = SubmitField('Post!')

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[InputRequired(),Length(min=3,max=20)])
	email = StringField('Email', validators=[InputRequired(),Email()])
	password = PasswordField('Password', validators=[InputRequired(),Length(min=6)])
	confirmPassword = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('password')])
	submit = SubmitField('Register!')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[InputRequired(),Email()])
	#username = StringField('Username',validators=[InputRequired(),Length(min=3,max=20)])
	password = PasswordField('Password', validators=[InputRequired(),Length(min=6)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login!')





