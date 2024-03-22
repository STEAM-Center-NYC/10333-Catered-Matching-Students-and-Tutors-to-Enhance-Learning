from flask import Flask, render_template, request, redirect
from dynaconf import Dynaconf
import pymysql
import pymysql.cursors
from pprint import pprint as print


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


@app.route("/", methods= ["GET", 'POST'])
def home():
    
    return render_template("index-page.html.jinja")


@app.route("/land", methods= ["GET", 'POST'])
def landing():

    return render_template("landing-page.html.jinja")

@app.route("/signin", methods= ["GET", 'POST'])
def SignIn():

    return render_template("sign-in-page.html.jinja")
