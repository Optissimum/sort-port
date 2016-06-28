from app import app, blueprint
from flask import render_template, redirect

app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/')
@app.route('/index')
def home():
    majorLinks = [('#1', 1),
                  ('#2', 2),
                  ('#3', 3),
                  ('#4', 4),]
    return render_template('index.html', majorLinks=majorLinks)
