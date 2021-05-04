from flask_bcrypt import Bcrypt
from haikuBlog import mysql


#Creating an object 
bcrypt = Bcrypt()

def hashPassword(password):
	return bcrypt.generate_password_hash(password).decode('utf-8')

def passwordMatch(hashedPassword,inputPassword):
	return bcrypt.check_password_hash(hashedPassword,inputPassword)	

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













