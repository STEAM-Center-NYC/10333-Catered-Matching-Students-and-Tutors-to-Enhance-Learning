from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
import flask_login
from dynaconf import Dynaconf
import flask_login

app = Flask(__name__)
app.secret_key = "J3D16GH"

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
    cursor.execute("SELECT * FROM `users` WHERE `id` = {user_id} ")
    result = cursor.fetchone()
    cursor.close
    get_db().commit()

    if result is None:
        return None
    
    return User(result["id"], result["username"])



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


def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(get_db, 'db'):
        get_db.db = connect_db()
    return get_db.db   

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(get_db, 'db'):
        get_db.db.close() 

@app.route("/", methods= ["GET", 'POST'])
def home():
    
    return render_template("index-page.html.jinja")


@app.route("/land", methods= ["GET", 'POST'])
def landing():

    return render_template("landing-page.html.jinja")



@app.route('/sign_in', methods = ['GET','POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form["email"]
        password = request.form["password"]
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `students` WHERE `student-email` = "{username}" ')
        cursor.execute(f'SELECT * FROM `tutors` WHERE `email` = "{password}" ')
        result = cursor.fetchone()
        cursor.close()
        get_db().commit()

        if password == result["password"]:
            user = load_user(result['email'])
            flask_login.login_user(user)
            return redirect('/')
    if flask_login.current_user.is_authenticated:
        return redirect("/")
    return render_template("signin-page.html.jinja")
