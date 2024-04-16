from flask import Flask, render_template, request, redirect, g
import pymysql
import pymysql.cursors
from dynaconf import Dynaconf
import flask_login
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


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
    is_authenticated = True
    is_auonymous = False
    is_active = True

    def __init__(self, id, email): 
        
        self.id = id
        self.email = email

    def get_id(self):
        return str(self.id)
        

@login_manager.user_loader
def load_user(user_id):
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE `id` = {user_id} ")
    result = cursor.fetchone()
    cursor.close
    get_db().commit()

    if result is None:
        return None
    
    return User(result["id"], result["email"])




class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

def connect_db():
    return pymysql.connect(
        host = "10.100.33.60",
        user = settings.db_user,
        password = settings.db_pass,
        database = settings.db_name,
        cursorclass = pymysql.cursors.DictCursor,
        autocommit = True
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
@flask_login.login_required
def home():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM `users` ')
    result = cursor.fetchall()
    cursor.close()
    return render_template("index-page.html.jinja", result =result)


@app.route("/land", methods= ["GET", 'POST'])
def landing():

    return render_template("landing-page.html.jinja")



@app.route('/signin', methods = ['GET','POST'])
def signin():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `users` WHERE `email` = "{email}" ')
        result = cursor.fetchone()
        cursor.close()
        get_db().commit()

        if password == result["password"]:
            user = load_user(result['id'])
            flask_login.login_user(user)
            return redirect('/')
    if flask_login.current_user.is_authenticated:
        return redirect("/")
    return render_template("signin-page.html.jinja")



@app.route("/signup", methods= ["GET", 'POST'])
def signup():
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
@flask_login.login_required
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
@flask_login.login_required
def profile():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        file_name = secure_filename(file.filename)
        user = flask_login.current_user
        cursor = get_db().cursor()
        cursor.execute(f"UPDATE users SET profile_img = '{file_name}' WHERE id = {user.id}")             
        cursor.close()
        return ("File has been uploaded.")  
    return render_template("profile.html.jinja", form=form)

@app.route("/profile/<id>", methods=["GET","POST"])
@flask_login.login_required
def public_profile(id):

    
    return render_template("profile.html.jinja")
