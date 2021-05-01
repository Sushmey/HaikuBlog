from flask import Flask, render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
import os
import syllapy
from dotenv import load_dotenv
from haikuInput import Haiku, LoginForm, RegistrationForm
from datetime import datetime
from flask_bcrypt import Bcrypt

#Creating an object 
bcrypt = Bcrypt()

def hashPassword(password):
	return bcrypt.generate_password_hash(password).decode('utf-8')

def passwordMatch(hashedPassword,inputPassword):
	return bcrypt.check_password_hash(hashedPassword,inputPassword)	

app = Flask(__name__)


load_dotenv('.env')

#SQL DB INfO
mysql = MySQL(app)
app.config['MYSQL_USER'] = os.getenv('USERNAME')
app.config['MYSQL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('HOST')
app.config['MYSQL_DB'] = os.getenv('DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




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
	if(form.validate_on_submit() and request.method=='POST'):
		cursor = mysql.connection.cursor()
		loginInfo = request.form
		email = loginInfo['email']
		inputPassword = loginInfo['password']
		cursor.execute("SELECT * FROM User WHERE email='{email}'".format(email=email))
		userInfo = cursor.fetchall()
		if(passwordMatch(userInfo[0]['password'],inputPassword)):
			flash('Logged in as {}'.format(userInfo[0]['username']),'success')
			return redirect('home')
		else:
			flash('Invalid email or password','danger')
	return render_template('login.html',title='Login', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if (form.validate_on_submit()and request.method=='POST'):
		cursor = mysql.connection.cursor()
		userDetails = request.form
		username = userDetails['username']
		email = userDetails['email']
		cursor.execute("SELECT * FROM User WHERE email='{email}'".format(email=email))
		emailCheck = cursor.fetchall()
		cursor.execute("SELECT * FROM User WHERE username='{username}'".format(username=username))
		usernameCheck = cursor.fetchall()
		if(emailCheck == () and usernameCheck == ()):
			password = hashPassword(userDetails['password'])
			cursor.execute("INSERT INTO User (username,email,password) VALUES(%s,%s,%s)",(username,email,password))
			mysql.connection.commit()
			cursor.close()
			flash('Account created for {}!'.format(form.username.data), 'success')
			return redirect(url_for('home'))
		elif(usernameCheck!=()):
			flash('Username is already taken', 'danger')		
		elif(emailCheck!=()):
			flash('Account already exists with that email', 'danger')			
	return render_template('register.html',title='Register', form=form)

if(__name__=='__main__'):  #This is so that we can run it directly in debug mode
	app.run(debug=True)    


			

