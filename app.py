from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
from pprint import pprint as print



app = Flask(__name__)

@app.route("/", methods= ["GET", 'POST'])
def landing():
    
    return render_template("landing.page.html.jinja")
