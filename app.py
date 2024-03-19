from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
from pprint import pprint as print



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

@app.route("/", methods= ["GET", 'POST'])
def home():
    
    return render_template("index-page.html.jinja")


@app.route("/land", methods= ["GET", 'POST'])
def landing():
    return render_template("landing-page.html.jinja")


@app.route("/signup-tutor", methods= ["GET", 'POST'])
def signup_tutor():
    return render_template("signup-tutor.html.jinja")
