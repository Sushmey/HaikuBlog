from flask import Flask
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

app = Flask(__name__)


SECRET_KEY = os.urandom(32)
# SECRET KEY to prevent modifying of cookies
app.config['SECRET_KEY'] = SECRET_KEY


load_dotenv('.env')

#SQL DB INfO
mysql = MySQL(app)
app.config['MYSQL_USER'] = os.getenv('USERNAME')
app.config['MYSQL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('HOST')
app.config['MYSQL_DB'] = os.getenv('DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


from haikuBlog import routes