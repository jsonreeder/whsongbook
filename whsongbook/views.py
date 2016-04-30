from . import app
from flask import render_template

@app.route("/")
def home():
    return render_template("song_fixed.html")

@app.route("/songs")
def songs():
    return "Hello, songs"
