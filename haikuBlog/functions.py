from flask_bcrypt import Bcrypt
from haikuBlog import mysql
from haikuBlog import os
import secrets
import syllapy
from haikuBlog import app
from PIL import Image



#Creating an object 
bcrypt = Bcrypt()

def hashPassword(password):
	return bcrypt.generate_password_hash(password).decode('utf-8')

def passwordMatch(hashedPassword,inputPassword):
	return bcrypt.check_password_hash(hashedPassword,inputPassword)	

def savePicture(picture,user):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_picx',picture_fn)

	#Checking to see if picture already exists so that we can just replace it instead of saving a new one
	prev_pic = os.path.join(app.root_path, 'static/profile_picx',user[0]['profile_img'])
	if (os.path.exists(prev_pic) and prev_pic != 'default.png'):
		os.remove(prev_pic)
	#Resizing the picture to save space 
	output_size = (125,125)
	i = Image.open(picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

def haikuFormatter(haiku):
	syllables=0
	words = haiku.split()
	haikuFormatted = ''
	for word in words:
		syllables += syllapy.count(word)
		if(syllables>= 5):
			if(syllables == 5):
				word = word+os.linesep	
			elif(syllables>=12):
				if(syllables==12):
					word = word+os.linesep
		haikuFormatted += ' '+word				
	haikuFormatted = haikuFormatted+os.linesep
	return haikuFormatted	













