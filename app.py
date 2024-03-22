from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
import flask_login
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_file =  ['settings.toml']
)

settings = Dynaconf(
    settings_file = ['settings.toml']
)

app = Flask(__name__)

def connect_db():
    return pymysql.connect(
        host = "10.100.33.60",
        user = settings.db_user,
        password = settings.db_pass,
        database = settings.db_name,
        cursorclass = pymysql.cursors.DictCursor,
        autocommit = True
    )


def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user= settings.db_user,
        password= settings.db_pass,
        database= settings.db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 

@app.route("/", methods= ["GET", 'POST'])
def home():
    
    return render_template("index-page.html.jinja")


@app.route("/land", methods= ["GET", 'POST'])
def landing():

    return render_template("landing-page.html.jinja")
