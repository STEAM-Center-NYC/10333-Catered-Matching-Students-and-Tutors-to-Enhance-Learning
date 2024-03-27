from flask import Flask,g
from flask import render_template,request, redirect
import pymysql
import pymysql.cursors
import flask_login
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_file =  ['settings.toml']
)


app = Flask(__name__)

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

@app.route("/contact", methods= ["GET", 'POST'])
def contact():
    
    return render_template("contact-page.html.jinja")




@app.route("/signup-students", methods= ["GET", 'POST'])
def signup_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        grade = request.form['grade']
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `students`(`student-name` , `student-email`, `password`, `gender`, `grade-level`) VALUES('{name}', '{email}', '{password}', '{gender}', '{grade}')")      
        cursor.close()
        get_db().commit()

    return render_template("signup-students.html.jinja")

@app.route("/signup-tutor", methods= ["GET", 'POST'])
def signup_tutor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        education = request.form['education']
        subject = request.form['subject']
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `tutors`(`name` , `email`, `password`, `gender`,`education-level`, `subject`) VALUES('{name}', '{email}', '{password}', '{gender}','{education}' ,'{subject}')")         
        cursor.close()
        get_db().commit()
    return render_template("signup-tutor.html.jinja")


@app.route("/match", methods= ["GET", 'POST'])
def matching():
    if request.method == 'POST':
        subjects = request.form['subject']
    
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `tutors` WHERE `subject` = "{subjects}"')
        results = cursor.fetchall()
        cursor.close()
    else:
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `tutors`')
        results = cursor.fetchall()
        cursor.close()

    return render_template("match.html.jinja", tutor_list = results)
