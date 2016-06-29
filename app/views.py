from app import app, blueprint
from flask import render_template, redirect

app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')
