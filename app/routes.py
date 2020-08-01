from flask import render_template, redirect, url_for
from app import app

user = {"username": "test@test.com",
        "logged_in": True}

nav = {"show_manage_documents": True,
       "show_create_access_code": True,
       "show_manage_access_code": True}


@app.route('/')
@app.route('/index')
def index():
    if user["logged_in"]:
        return redirect(url_for('account_home'))
    else:
        return render_template('index.html', user=user)


@app.route('/test')
def test():
    return "Test Link!"


# New Account Processes


@app.route('/new_account_signup')
def new_account_signup():
    return render_template('new_account/new_account_signup.html')


@app.route('/new_account_click_link')
def new_account_click_link():
    return render_template('new_account/new_account_signup_clicklink.html')


# Existing Account Processes


@app.route('/account')
def account_home():
    return render_template('account_home.html', user=user, nav=nav)


# New Document Processes


@app.route('/new_document_1')
def new_document_selection():
    return render_template('add_document/add_doc_1_selection.html', user=user, nav=nav)



