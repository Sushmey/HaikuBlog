from flask import render_template, url_for, request, flash, redirect, g, session
from haikuBlog import app
import syllapy
from haikuBlog.haikuInput import Haiku, LoginForm, RegistrationForm, ProfileUpdateForm
import ast
from haikuBlog import mysql
from haikuBlog.functions import hashPassword, passwordMatch, savePicture, haikuFormatter

from flask_login import login_user

@app.route('/')
@app.route('/home')
def home():
	cursor = mysql.connection.cursor()
	cursor.execute("SELECT * FROM Posts INNER JOIN User ON Posts.user_id = User.user_id ORDER BY date_posted DESC")
	posts = cursor.fetchall()
	return render_template('home.html',title='Home',posts=posts)

@app.route('/post/new',methods=['GET','POST'])
def postHaiku():
	if('user_id' in session):
		form = Haiku()
		if(form.validate_on_submit() and request.method=='POST'):
			inputHaiku = request.form
			haiku = haikuFormatter(inputHaiku['haiku'])
			title = inputHaiku['title']
			cursor = mysql.connection.cursor()
			cursor.execute("INSERT INTO Posts (title,content,user_id) VALUES(%s,%s,%s)",(title,haiku,session['user_id']))
			mysql.connection.commit()
			cursor.close()
			flash('Your haiku has been uploaded!','success')
			return redirect(url_for('home'))
		return render_template('inputPage.html',title='Add', form=form )
	else:
		return redirect(url_for('login'))
			

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
			#session['mode'] = 'light' #Dark mode
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



@app.route('/profile',methods=['GET','POST'])
def profile():
	if('user_id' in session):
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM Posts INNER JOIN User ON Posts.user_id = User.user_id WHERE User.user_id='{user_id}'".format(user_id=session['user_id']))
		userPosts = cursor.fetchall()
		form = ProfileUpdateForm()
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM User WHERE user_id='{user_id}'".format(user_id=session['user_id']))
		user = cursor.fetchall()
		profile_image = url_for('static',filename='profile_picx/'+user[0]['profile_img'])
		if(form.validate_on_submit()):
			print(form.pfp.data)
			if(form.username.data == user[0]['username'] and form.email.data == user[0]['email'] and (form.pfp.data == user[0]['profile_img'] or form.pfp.data==None)):
				flash('User info is same, no change','danger')
				return redirect(url_for('profile'))	
			if(form.pfp.data):
				profile_image = savePicture(form.pfp.data,user)
				cursor.execute("UPDATE User SET profile_img='{profile_image}' WHERE user_id='{user_id}'".format(profile_image=profile_image,user_id = session['user_id']))  	
			cursor.execute("UPDATE User SET username = '{username}', email='{email}' WHERE user_id='{user_id}'".format(user_id=session['user_id'],username=form.username.data,email=form.email.data))
			mysql.connection.commit()
			flash('Account info has been updated!', 'success')
			return redirect(url_for('profile'))
		elif(request.method=='GET'):
			form.username.data = user[0]['username']
			form.email.data = user[0]['email']	
		cursor.close()
		return render_template('profile.html',title='Profile',user=user,profile_image=profile_image, form=form, userPosts=userPosts)
	else:
		return redirect(url_for('login'))	


@app.route('/posts/edit',methods=['GET','POST'])
def edit():
	if('user_id' in session):
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM Posts INNER JOIN User ON Posts.user_id = User.user_id WHERE User.user_id='{user_id}' ORDER BY date_posted DESC".format(user_id=session['user_id']))
		userPosts = cursor.fetchall()
		cursor.close()
		if(request.method=='POST'):
			cursor = mysql.connection.cursor()
			postID=int(request.form['postId'])
			cursor.execute("SELECT * FROM Posts WHERE post_id='{postId}'".format(postId=postID))
			if(cursor.fetchall()):
				cursor.execute("DELETE FROM Posts WHERE post_id='{postId}'".format(postId=postID))
				mysql.connection.commit()
				flash('Post has been deleted!','success')
			else:
				flash("Post doesn't exist, nothing is deleted",'danger')			
			cursor.close()
			return redirect(url_for('edit'))
		return render_template('edit.html',title='Edit',userPosts=userPosts)
	else:		
		return redirect(url_for('login'))	




@app.route('/logout')
def logout():
	if('user_id' in session):
		session.pop('user_id',None)
	flash('Logout successful!', 'success')	
	return redirect(url_for('login'))	




@app.route('/about')
def about():
	return render_template('about.html',title='about')









