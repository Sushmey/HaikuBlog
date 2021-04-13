from flask import Flask, render_template, url_for, request
import os
from haikuInput import Haiku
app = Flask(__name__)


SECRET_KEY = os.urandom(32)
# SECRET KEY to prevent modifying of cookies
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def hello_world():
    return render_template('home.html',title='Home')

@app.route('/addhaiku',methods=['GET','POST'])
def haikuInput():
	form = Haiku()
	if(form.validate_on_submit() and request.method=='POST'):
		inputHaiku = request.form
		print(inputHaiku['haiku'])
	return render_template('inputPage.html',title='Add', form=form )

if(__name__=='__main__'):  #This is so that we can run it directly in debug mode
	app.run(debug=True)    