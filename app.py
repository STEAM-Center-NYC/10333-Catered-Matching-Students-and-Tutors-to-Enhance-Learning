from flask import Flask,g
from flask import render_template,request, redirect
import pymysql
import pymysql.cursors
import flask_login




app = Flask(__name__)

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="achen",
        password="232126110",
        database="tutoria",
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


@app.route("/signup-tutor", methods= ["GET", 'POST'])
def signup_tutor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        education = request.form['education']
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `tutors`(`name` , `email`, `password`, `gender`,`education-level`) VALUES('{name}', '{email}', '{password}', '{gender}','{education}')")         
        cursor.close()
        get_db().commit()


    return render_template("signup-tutor.html.jinja")
