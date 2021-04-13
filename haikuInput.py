from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import syllapy


def validate_haiku(form,haiku):
	words = haiku.data.split()
	syllables = 0
	for word in words:
		word = word.lower()
		syllables+=syllapy.count(word)
	if (syllables != 17 ):
		raise ValidationError("Check the number of syllables")		


class Haiku(FlaskForm):
	haiku = StringField('Haiku',validators=[InputRequired(), validate_haiku])

	submit = SubmitField('Post!')




