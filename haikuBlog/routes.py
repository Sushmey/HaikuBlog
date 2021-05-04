from flask import render_template, url_for, request, flash, redirect, g, session
from haikuBlog import app
import syllapy
from haikuBlog.haikuInput import Haiku, LoginForm, RegistrationForm

from haikuBlog import mysql
from haikuBlog.functions import hashPassword, passwordMatch

from flask_login import login_user

posts = [{'haiku':'Bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh bruh',
		'author':'author'	
		},{}]




@app.before_request
def before_request():  #This function checks if theres a user in session before it sends a request 
	cursor = mysql.connection.cursor()
	g = None
	if 'user_id' in session:  #If there is a user then it stores the user data in a global request variable imported from flask, called g
		cursor.execute("SELECT user_id,username FROM User WHERE user_id='{user_id}'".format(user_id=session['user_id']))
		user = cursor.fetchall()
		g = user[0]['user_id'] 
	cursor.close()	




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
		session.pop('user_id',None)
		cursor = mysql.connection.cursor()
		loginInfo = request.form
		email = loginInfo['email']
		inputPassword = loginInfo['password']
		cursor.execute("SELECT * FROM User WHERE email='{email}'".format(email=email))
		userInfo = cursor.fetchall()
		if(passwordMatch(userInfo[0]['password'],inputPassword)):
			session['user_id'] = userInfo[0]['user_id']
			flash('Logged in as {}'.format(userInfo[0]['username']),'success')
			cursor.close()
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
			return redirect(url_for('login'))				
	return render_template('register.html',title='Register', form=form)



@app.route('/profile')
def profile():
	if('user_id' in session):
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM User WHERE user_id='{user_id}'".format(user_id=session['user_id']))
		user = cursor.fetchall()
		return render_template('profile.html',title='Profile',user=user)
	else:
		return redirect(url_for('login'))	

@app.route('/logout')
def logout():
	if('user_id' in session):
		session.pop('user_id',None)
	return redirect(url_for('login'))	














