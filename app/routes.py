from flask import render_template, redirect, url_for
from app import app

user = {"username": "test@test.com",
        "logged_in": False}

nav = {"show_nav": True,
       "show_manage_documents": True,
       "show_create_access_code": True,
       "show_manage_access_code": True}


@app.route('/')
@app.route('/index')
def index():
    if user["logged_in"]:
        return redirect(url_for('account_home'))
    else:
        return render_template('index.html', user=user, nav=nav)


@app.route('/test')
def test():
    return "Test Link!"


# General Pages


@app.route('/about')
def about():
    return render_template('general/about.html', user=user, nav=nav)


@app.route('/how_it_works')
def how_it_works():
    return render_template('general/how_it_works.html', user=user, nav=nav)


@app.route('/faq')
def faq():
    return render_template('general/faq.html', user=user, nav=nav)


@app.route('/contact')
def contact():
    return render_template('general/contact.html', user=user, nav=nav)


# New Account Processes


@app.route('/new_account_signup')
def new_account_signup():
    if user["logged_in"]:
        return redirect(url_for('account_home'))
    else:
        return render_template('new_account/new_account_signup.html', nav=nav)


@app.route('/new_account_click_link')
def new_account_click_link():
    if user["logged_in"]:
        return redirect(url_for('account_home'))
    else:
        return render_template('new_account/new_account_signup_clicklink.html', nav=nav)


# Existing Account Processes


@app.route('/account')
def account_home():
    return render_template('account_home.html', user=user, nav=nav)


@app.route('/edit_profile')
def edit_profile():
    return render_template('profile/edit_profile.html', user=user, nav=nav)


@app.route('/logout')
def logout():
    nav["logged_in"] = False
    return redirect(url_for('index'))


# New Document Processes


@app.route('/new_document_1')
def new_document_selection():
    return render_template('add_document/add_doc_1_selection.html', user=user, nav=nav)


@app.route('/new_document_2')
def new_document_upload_image():
    return render_template('add_document/add_doc_2_upload_image.html', user=user, nav=nav)


@app.route('/new_document_3')
def new_document_confirm_image():
    return render_template('add_document/add_doc_3_confirm_image.html', user=user, nav=nav)


@app.route('/new_document_4')
def new_document_add_personal_details():
    return render_template('add_document/add_doc_4_add_personal_details.html', user=user, nav=nav)


@app.route('/new_document_5')
def new_document_confirm_personal_details():
    return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user, nav=nav)


@app.route('/new_document_6')
def new_document_add_document_details():
    return render_template('add_document/add_doc_6_add_document_details.html', user=user, nav=nav)


@app.route('/new_document_7')
def new_document_confirm_document_details():
    return render_template('add_document/add_doc_7_confirm_document_details.html', user=user, nav=nav)


@app.route('/new_document_8')
def new_document_finish():
    return render_template('add_document/add_doc_8_finish.html', user=user, nav=nav)


# New Document Processes


@app.route('/manage_all_documents')
def manage_all_documents():
    return render_template('manage_documents/manage_all_documents.html', user=user, nav=nav)


@app.route('/manage_document')
def manage_document():
    return render_template('manage_documents/manage_document.html', user=user, nav=nav)


# Generate New Access Code Processes


@app.route('/generate_access_code_1')
def generate_code_document_selection():
    return render_template('generate_access_code/generate_code_1_selection.html', user=user, nav=nav)


@app.route('/generate_access_code_2')
def generate_code_access_details():
    return render_template('generate_access_code/generate_code_2_details.html', user=user, nav=nav)


@app.route('/generate_access_code_3')
def generate_code_confirm_access_details():
    return render_template('generate_access_code/generate_code_3_confirm_details.html', user=user, nav=nav)


# Manage Access Codes Processes


@app.route('/manage_code')
def manage_access_code():
    return render_template('manage_access_code/manage_code.html', user=user, nav=nav)


@app.route('/manage_all_codes')
def manage_all_access_codes():
    return render_template('manage_access_code/manage_all_codes.html', user=user, nav=nav)


# Errors


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', user=user, nav=nav)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', user=user, nav=nav)

