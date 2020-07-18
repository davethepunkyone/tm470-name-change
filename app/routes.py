from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {"username": "dave"}
    return render_template('index.html', user=user)


@app.route('/test')
def test():
    return "Test Link!"
