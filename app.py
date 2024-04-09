from flask import Flask,g
from flask import render_template,request, redirect
import pymysql
import pymysql.cursors
from dynaconf import Dynaconf
import random
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
import wtforms
from werkzeug.utils import secure_filename
import os



settings = Dynaconf(
    settings_file =  ['settings.toml']
)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jhbgdifjhujne3hr3@#J$JERri32@%j4#FLD?SRJF#ORJ$D>R>>$%K$GRIFJTi4OJrhjedfdsojfrSHTIREJHTOJRSJLFN568785345=--213;'
app.config['UPLOAD_FOLDER'] = 'media'

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

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




@app.route("/signup", methods= ["GET", 'POST'])
def signup_tutor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        education = request.form['education']
        subject = request.form['subject']
        role = request.form['role']
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `users`(`name` , `email`, `password`, `gender`,`educational_level`, `subject`,`role`) VALUES('{name}', '{email}', '{password}', '{gender}','{education}' ,'{subject}','{role}')")             
        cursor.close()
        get_db().commit()
    return render_template("signup.html.jinja")


@app.route("/match", methods= ["GET", 'POST'])  
def matching():
    if request.method == 'POST':
        subjects = request.form['subject']
        """if subjects == 'Choose...':
            
            return render_template("match.html.jinja", tutor_list = results2)
        else:"""
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `users` WHERE `subject` = "{subjects}" AND `role` = "tutor"')
        results = cursor.fetchall()
        results = random.choice(results)
        cursor.close()
    else:
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `tutors`')
        results = cursor.fetchall()
        cursor.close()

    return render_template("match.html.jinja", tutor_list = results)

@app.route("/profile", methods=["GET","POST"])
def profile():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        file_name = secure_filename(file.filename)
        cursor = get_db().cursor()
        cursor.execute(f"UPDATE users SET profile_img = {file_name} WHERE ')")             
        cursor.close()
        return ("File has been uploaded.")  
    return render_template("profile.html.jinja", form=form)
