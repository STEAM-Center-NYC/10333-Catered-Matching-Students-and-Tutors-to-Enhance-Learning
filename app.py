from flask import Flask, render_template, request, redirect, g, flash,url_for,send_from_directory
import pymysql
import pymysql.cursors
from dynaconf import Dynaconf
import flask_login
import random
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
import os
import werkzeug.exceptions




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

    def __init__(self, id, email, dob, gender , subject, educational_level, role, name): 
        
        self.id = id
        self.email = email
        self.dob = dob
        self.gender = gender
        self.subject = subject
        self.educational_level = educational_level
        self.role = role
        self.name = name

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
    
    return User(result["id"], result["email"],result['dob'],result['gender'],result['subject'],result['educational_level'],result['role'],result['name'])

@login_manager.unauthorized_handler
def unauthorized():
    return render_template("unauthorized_error.html.jinja")


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

@app.route("/home", methods= ["GET", 'POST'])
@flask_login.login_required
def home():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM `users` WHERE `role` = "tutor"')
    result = cursor.fetchall()
    cursor.close()
    cursor = get_db().cursor()
    user = flask_login.current_user
    cursor.execute(f'SELECT * FROM `users` WHERE `id` = "{user.id}"')
    result2 = cursor.fetchone()
    cursor.close() 
    return render_template("index-page.html.jinja", result =result, user = result2)


@app.route("/", methods= ["GET", 'POST'])
def landing():
    cursor = get_db().cursor()
    user = flask_login.current_user
    cursor.execute(f'SELECT * FROM `users` WHERE `id` = "{user.id}"')
    result = cursor.fetchone()
    cursor.close() 
    return render_template("landing-page.html.jinja", result = result)



@app.route('/signin', methods = ['GET','POST'])
def signin():
    try:
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
                return redirect('/home')
            if flask_login.current_user.is_authenticated:
                return redirect("/home")
    except TypeError:
        flash("Incorrect Username or Password")
    
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
        date = request.form['date']
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `users`(`name` , `email`, `password`, `gender`,`educational_level`,`subject`,`role`,`dob`) VALUES('{name}', '{email}', '{password}', '{gender}','{education}' ,'{subject}','{role}','{date}')")             
        cursor.close()
        get_db().commit()
        return redirect("signin-page.html.jinja")
    return render_template("signup.html.jinja")


@app.route("/match", methods= ["GET", 'POST'])  
@flask_login.login_required
def matching():
    if request.method == 'POST':
        subjects = request.form['subject']
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
    cursor = get_db().cursor()
    user = flask_login.current_user
    cursor.execute(f'SELECT * FROM `users` WHERE `id` = "{user.id}"')
    result = cursor.fetchone()
    cursor.close() 
    return render_template("match.html.jinja", tutor_list = results, result = result)

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
        flash("File has been uploaded") 
    cursor = get_db().cursor()
    user = flask_login.current_user
    cursor.execute(f'SELECT * FROM `users` WHERE `id` = "{user.id}"')
    result = cursor.fetchone()
    cursor.close() 
    return render_template("profile.html.jinja", form=form, result= result)

@app.route("/profile/<id>", methods=["GET","POST"])
@flask_login.login_required
def public_profile(id):
    cursor = get_db().cursor()
    cursor.execute(f'SELECT * FROM `users` WHERE `id` = {id}')
    result = cursor.fetchone()
    cursor.close()
    cursor = get_db().cursor()
    cursor.execute(f'SELECT * FROM `ratings` INNER JOIN `users` ON ratings.user = users.id WHERE `profile` = {id} ')
    review = cursor.fetchall()
    cursor = get_db().cursor()
    cursor.execute(f'SELECT AVG(rating) FROM ratings WHERE `profile` = {id}')
    rating = cursor.fetchone()
    
    cursor.close()
    user = flask_login.current_user

    try:
        if request.method == 'POST':
            ratings = request.form['rating']
            review = request.form['review']
            cursor = get_db().cursor()
            cursor.execute(f"INSERT INTO `ratings`(`profile` ,`user`, `rating`,`review` ) VALUES('{id}','{user.id}','{ratings}','{review}')")
            cursor.close() 
    except pymysql.err.IntegrityError:
        return render_template("review_error.html.jinja", id = id)
    except werkzeug.exceptions.BadRequestKeyError:
        flash("Please Fill Out The Form Before Submitting")
    
    return render_template("public_profile.html.jinja", result = result , review = review, rating = rating)


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )
  

@app.route("/edit",methods=["GET","POST"])
@flask_login.login_required
def edit():
    user = flask_login.current_user
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        education = request.form['education']
        subject = request.form['subject']
        date = request.form['date']
        linkedin = request.form['linkedin']
        cursor = get_db().cursor()
        cursor.execute(f"UPDATE `users` SET name = '{name}', email = '{email}', gender = '{gender}', educational_level = '{education}', subject = '{subject}',  dob = '{date}', linkedin = '{linkedin}'  WHERE `id` = {user.id} ")             
        cursor.close()
        return redirect("/profile")
    
    get_db().commit()
    cursor = get_db().cursor()
    cursor.execute(f'SELECT * FROM `users` WHERE `id` = {user.id}')
    result = cursor.fetchone()
    cursor.close()
    return render_template("edit.html.jinja", result = result)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    cursor = get_db().cursor()
    user = flask_login.current_user
    cursor.execute(f'SELECT * FROM `users` WHERE `id` = "{user.id}"')
    result2 = cursor.fetchone()
    cursor.close() 
    return render_template("contact-page.html.jinja", user = result2)


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("/signin")

@app.route("/dm/<id>", methods=["GET", "POST"])
def dm(id):
    cursor = get_db().cursor()
    cursor.execute(f'SELECT * FROM `users` WHERE `id` = {id}')
    result = cursor.fetchone()
    cursor.close()
    if request.method == 'POST':
        user = flask_login.current_user
        message = request.form['Message']
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `dm` (`message_text`, `sender_id`, `receiver_id`) VALUES('{message}','{user.id}','{result['id']}')")
    return render_template("Direct-Message.html.jinja", result = result)
