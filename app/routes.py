from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {"username": "dave"}
    return render_template('index.html', user=user)


@app.route('/new_account_signup')
def new_account_signup():
    return render_template('new_account/new_account_signup.html')


@app.route('/new_account_click_link')
def new_account_click_link():
    return render_template('new_account/new_account_signup_clicklink.html')


@app.route('/account')
def account_home():
    user = {"username": "dave"}
    return render_template('account_home.html', user=user)


@app.route('/test')
def test():
    return "Test Link!"
