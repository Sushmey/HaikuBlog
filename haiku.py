from flask import Flask, render_template, url_for, request
import os
import syllapy
from haikuInput import Haiku
app = Flask(__name__)


SECRET_KEY = os.urandom(32)
# SECRET KEY to prevent modifying of cookies
app.config['SECRET_KEY'] = SECRET_KEY

posts = [{'haiku':'Bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh',
		'author':'author'	
		},{}]
def haikuFormatter(haiku):
	syllables=0
	words = haiku.split()
	haikuFormatted = ''
	for word in words:
		print(word)
		syllables += syllapy.count(word)
		if(syllables>= 5):
			if(syllables == 5):
				word = word+os.linesep	
			elif(syllables>=12):
				if(syllables==12):
					word = word+os.linesep
		haikuFormatted += ' '+word				
	haikuFormatted = haikuFormatted+os.linesep
	print('Formated haiku : ')
	print(haikuFormatted)
	return haikuFormatted	

@app.route('/')
def hello_world():
    return render_template('home.html',title='Home',posts=posts)

@app.route('/addhaiku',methods=['GET','POST'])
def haikuInput():
	form = Haiku()
	if(form.validate_on_submit() and request.method=='POST'):
		inputHaiku = request.form
		print(inputHaiku['haiku'])
		haiku = haikuFormatter(inputHaiku['haiku'])
		print(haiku)
		author = 'author'
		posts =[{'haiku':haiku,'author':author},{}]
	return render_template('inputPage.html',title='Add', form=form )

if(__name__=='__main__'):  #This is so that we can run it directly in debug mode
	app.run(debug=True)    


			

