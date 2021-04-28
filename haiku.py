from flask import Flask, render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
import os
import syllapy
#from dotenv import load_dotenv
from haikuInput import Haiku, LoginForm, RegistrationForm
app = Flask(__name__)


#load_dotenv('.env')

#SQL DB INfO
app.config['MYSQL_USER'] = os.environ.get("USERNAME")
app.config['MYSQL_PASSWORD'] = os.environ.get("PASSWORD")
app.config['MYSQL_HOST'] = os.environ.get("DOMAIN")
app.config['MYSQL_DB'] = os.environ.get("DB")
app.config['MYSQL_CURSORCLASS'] = 'Dict'



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
			print(syllables)
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
@app.route('/home')
def home():
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

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if(form.validate_on_submit()):
		if(form.email.data=='admin@haiku.com' and form.password.data=='haikus'):
			flash('Logged in as {}'.format('admin'),'success')
			return redirect('home')
		else:
			flash('Invalid email or password','danger')
	return render_template('login.html',title='Login', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if (form.validate_on_submit()):
		flash('Account created for {}!'.format(form.username.data), 'success')
		return redirect(url_for('home'))
	return render_template('register.html',title='Register', form=form)

if(__name__=='__main__'):  #This is so that we can run it directly in debug mode
	app.run(debug=True)    


			

