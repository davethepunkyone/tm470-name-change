from flask import render_template, redirect, url_for, request
from app import app
import datetime
import globals.mock_variables as mock

from classes.user_class import User
from classes.signup_verification_class import SignupVerification
from classes.document_class import Document
from classes.marriagecertificate_class import MarriageCertificate
from classes.deedpoll_class import DeedPoll
from classes.decreeabsolute_class import DecreeAbsolute
from classes.accesscode_class import AccessCode
from classes.enums import VerifiedStates, AccessStates
from functions.org_functions import return_specific_org_from_list
from functions.access_code_functions import generate_unique_access_code
from functions.signup_functions import generate_signup_code, email_user_notepad_version

from functions import logging_functions as logger

# Global Lists
users_list = mock.mock_list_of_users()
orgs = mock.mock_list_of_organisations()
signup_verification_list = []

# Global Instances
user = User()
document = Document()
access_code = AccessCode()

# Incrementer
incrementer_user = 1000
incrementer_document = 8000
incrementer_access_code = 5000

# Other Globals
success_message = None
failure_message = None


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    global user, failure_message
    if user.logged_in:
        return redirect(url_for('account_home'))
    else:
        if request.method == 'GET':
            logger.log_benchmark("Load Homepage")
            feedback = failure_message
            failure_message = None
            return render_template('index.html', user=user, feedback=feedback)
        elif request.method == 'POST':
            logger.log_benchmark("Homepage - Attempt Login")
            if len(request.form) > 0:
                email = request.form["email_address"]
                pwd = request.form["password"]
                if email == "" or pwd == "":
                    feedback = "You need to provide your email and password to log in."
                    return render_template('index.html', user=user, feedback=feedback)
                else:
                    try:
                        user = return_logged_in_user(email, pwd)
                    except LookupError as err:
                        feedback = err
                        return render_template('index.html', user=user, feedback=feedback)
                    if not user.verified_state:
                        return redirect(url_for('new_account_click_link'))
                    else:
                        user.logged_in = True
                        return redirect(url_for('account_home'))
            else:
                feedback = "You need to provide your email and password to log in."
                return render_template('index.html', user=user, feedback=feedback)


def return_logged_in_user(email: str, pwd: str) -> User:
    for user_check in users_list:
        if user_check.email == email:
            if user_check.prototype_password == pwd:
                return user_check
            else:
                raise LookupError("The password for the user is not correct.")
    else:
        raise LookupError("The email address specified is not registered with this service.")


@app.route('/test/<test_conditions>')
def test(test_conditions):
    global user
    user = User()
    if test_conditions == "1":
        user = users_list.__getitem__(0)
        user.logged_in = True
    elif test_conditions == "2":
        user = users_list.__getitem__(1)
        user.logged_in = True
    elif test_conditions == "3":
        user = users_list.__getitem__(2)
        user.logged_in = True
    return redirect(url_for('index'))


# General Pages


@app.route('/about')
def about():
    return render_template('general/about.html', user=user)


@app.route('/how_it_works')
def how_it_works():
    return render_template('general/how_it_works.html', user=user)


@app.route('/faq')
def faq():
    return render_template('general/faq.html', user=user)


@app.route('/contact')
def contact():
    return render_template('general/contact.html', user=user)


# New Account Processes


@app.route('/new_account_signup', methods=['GET', 'POST'])
def new_account_signup():
    global user, incrementer_user

    if user.logged_in:
        return redirect(url_for('account_home'))
    else:
        if request.method == 'GET':
            logger.log_benchmark("Load New Account Signup")
            return render_template('new_account/new_account_signup.html', user=user)
        elif request.method == 'POST':
            logger.log_benchmark("New Account Signup - Submit Form")
            if len(request.form) > 0:
                forenames = request.form["forenames"]
                surname = request.form["surname"]
                email = request.form["email"]
                email_confirm = request.form["email_confirm"]
                pwd = request.form["password"]
                pwd_confirm = request.form["password_confirm"]
                capcha = request.form["capcha"]
                initial_feedback = check_new_user_form_values(forenames, surname, email, email_confirm, pwd,
                                                              pwd_confirm, capcha)
                if initial_feedback is not None:
                    feedback = initial_feedback
                    return render_template('new_account/new_account_signup.html', user=user, feedback=feedback)
                if not request.form.__contains__("agreement"):
                    feedback = "You must agree to the terms and conditions to proceed."
                    return render_template('new_account/new_account_signup.html', user=user, feedback=feedback)
                else:
                    user = User(user_id=incrementer_user, forenames=forenames, surname=surname, email=email,
                                prototype_password=pwd, verified_state=False)
                    users_list.append(user)
                    incrementer_user += 1
                    signup_details = SignupVerification(signup_code=generate_signup_code(), user_id=user.user_id)
                    signup_verification_list.append(signup_details)
                    email_user_notepad_version(user, signup_details)
                    return redirect(url_for('new_account_click_link'))
            else:
                feedback = "You need to complete all the fields to create a new account."
                return render_template('new_account/new_account_signup.html', user=user, feedback=feedback)


def check_new_user_form_values(forenames: str, surname: str, email: str, email_confirm: str, pwd: str,
                               pwd_confirm: str, capcha: str):
    if forenames == "" or surname == "" or email == "" or email_confirm == "" or pwd == "" or \
            pwd_confirm == "" or capcha == "":
        feedback = "You need to complete all the fields to create a new account."
    elif email != email_confirm:
        return "The email address and confirm email address do not match."
    elif pwd != pwd_confirm:
        return "The password and confirm password do not match."
    elif check_user_already_exists(email):
        return "The email address provided is already registered on this service."
    else:
        return None


def check_user_already_exists(email: str) -> bool:
    email_present = False
    for user_check in users_list:
        if user_check.email == email:
            email_present = True
            break
    return email_present


@app.route('/new_account_click_link')
def new_account_click_link():
    global success_message

    if user.logged_in:
        return redirect(url_for('account_home'))
    else:
        feedback = success_message
        success_message = None
        return render_template('new_account/new_account_signup_clicklink.html', user=user, feedback=feedback)


@app.route('/resend_account_email')
def resend_new_account_email():
    global success_message

    if user.logged_in:
        return redirect(url_for('account_home'))
    else:
        for signup_user in signup_verification_list:
            if signup_user.user_id == user.user_id:
                signup_details = signup_user
                email_user_notepad_version(user, signup_details)
                success_message = "Email has been resent."
                return redirect(url_for('new_account_click_link'))
        else:
            return redirect(url_for('index'))


@app.route('/new_account_confirm/<confirm_code>')
def new_account_confirm_code(confirm_code):
    global user, signup_verification_list, failure_message

    for signup_user in signup_verification_list:
        if signup_user.signup_code == confirm_code:
            user = retrieve_user_from_list(signup_user.user_id)
            user.verified_state = True
            user.logged_in = True
            signup_verification_list.remove(signup_user)
            return redirect(url_for('account_home'))
    else:
        failure_message = "The code provided in the link clicked is not valid."
        return redirect(url_for('index'))


def retrieve_user_from_list(user_id: int):
    global users_list

    for user_in_list in users_list:
        if user_in_list.user_id == user_id:
            return user_in_list
    else:
        raise LookupError("The user being queried is not in the list.")


# Existing Account Processes


@app.route('/account')
def account_home():
    if not user.logged_in:
        return redirect(url_for('index'))
    else:
        return render_template('account_home.html', user=user)


@app.route('/edit_profile')
def edit_profile():
    if not user.logged_in:
        return redirect(url_for('index'))
    else:
        return render_template('profile/edit_profile.html', user=user)


@app.route('/logout')
def logout():
    global user
    user = User()
    return redirect(url_for('index'))


# New Document Processes


@app.route('/new_document_1', methods=['GET', 'POST'])
def new_document_selection():
    global document, incrementer_document

    if user.logged_in:
        marriage_cert_present = False
        for user_doc in user.docs:
            if user_doc.document_type == "Marriage Certificate":
                marriage_cert_present = True

        if request.method == 'GET':
            return render_template('add_document/add_doc_1_selection.html', user=user, divorce_on=marriage_cert_present)
        elif request.method == 'POST':
            if len(request.form) > 0:
                access_code_id_doc = request.form["doc_type"]
                if access_code_id_doc == "marriage_cert":
                    document = MarriageCertificate(document_id=incrementer_document, user_id=user.user_id,
                                                   complete=False)
                    incrementer_document += 1
                    return redirect(url_for('new_document_upload_image'))
                elif access_code_id_doc == "deed_poll":
                    document = DeedPoll(document_id=incrementer_document, user_id=user.user_id, complete=False)
                    incrementer_document += 1
                    return redirect(url_for('new_document_upload_image'))
                elif access_code_id_doc == "decree_absolute":
                    document = DecreeAbsolute(document_id=incrementer_document, user_id=user.user_id, complete=False)
                    incrementer_document += 1
                    return redirect(url_for('new_document_upload_image'))  # TODO - Extra Page for decree absolute
                else:
                    feedback = "You need to select a valid option to proceed."
                    return render_template('add_document/add_doc_1_selection.html', user=user,
                                           divorce_on=marriage_cert_present, feedback=feedback)
            else:
                feedback = "You need to select an option to proceed."
                return render_template('add_document/add_doc_1_selection.html', user=user,
                                       divorce_on=marriage_cert_present, feedback=feedback)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_1a')
def new_document_decree_absolute_certificate():
    if user.logged_in:
        return render_template('add_document/add_doc_1_selection.html', user=user, doc=document)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_2')
def new_document_upload_image():
    if user.logged_in:
        return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_3')
def new_document_confirm_image():
    if user.logged_in:
        return render_template('add_document/add_doc_3_confirm_image.html', user=user, doc=document)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_4')
def new_document_add_personal_details():
    if user.logged_in:
        return render_template('add_document/add_doc_4_add_personal_details.html', user=user, doc=document)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_5')
def new_document_confirm_personal_details():
    if user.logged_in:
        return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user, doc=document)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_6')
def new_document_add_document_details():
    if user.logged_in:
        return render_template('add_document/add_doc_6_add_document_details.html', user=user, doc=document)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_7')
def new_document_confirm_document_details():
    if user.logged_in:
        return render_template('add_document/add_doc_7_confirm_document_details.html', user=user, doc=document)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_8')
def new_document_finish():
    if user.logged_in:
        return render_template('add_document/add_doc_8_finish.html', user=user, doc=document)
    else:
        return redirect(url_for('index'))


# New Document Processes


@app.route('/manage_all_documents')
def manage_all_documents():
    if user.logged_in:
        return render_template('manage_documents/manage_all_documents.html', user=user)
    else:
        return redirect(url_for('index'))


@app.route('/manage_document/<doc_id>')
def manage_document(doc_id):
    if user.logged_in:
        doc_to_manage = None
        for document in user.docs:
            if document.document_id == int(doc_id):
                doc_to_manage = document
                break

        if doc_to_manage is not None:
            return render_template('manage_documents/manage_document.html', user=user, doc=doc_to_manage)
        else:
            return redirect(url_for('manage_all_documents'))
    else:
        return redirect(url_for('index'))


# Generate New Access Code Processes


@app.route('/generate_access_code_1', methods=['GET', 'POST'])
def generate_code_document_selection():
    global access_code, user

    if user.logged_in:
        if request.method == 'GET':
            logger.log_benchmark("Generate Access Code (Start - Document Selection)")
            access_code = AccessCode()
            return render_template('generate_access_code/generate_code_1_selection.html', user=user)
        elif request.method == 'POST':
            if len(request.form) > 0:
                access_code_id_doc = request.form["user_doc"]
                access_code.uploaded_document = user.get_specific_listed_doc(int(access_code_id_doc))
                return redirect(url_for('generate_code_access_details'))
            else:
                feedback = "You need to select at least one option."
                return render_template('generate_access_code/generate_code_1_selection.html', user=user,
                                       feedback=feedback)
    else:
        return redirect(url_for('index'))


@app.route('/generate_access_code_2', methods=['GET', 'POST'])
def generate_code_access_details():
    global access_code, user

    if user.logged_in:
        feedback = ""
        if request.method == 'GET':
            logger.log_benchmark("Generate Access Code (Page 2 - Access Details)")
            return render_template('generate_access_code/generate_code_2_details.html', user=user,
                                   code_to_use=access_code, orgs=orgs)
        elif request.method == 'POST':
            if len(request.form) > 0:
                if request.form["org"] == "":
                    feedback = "You need to select an organisation."
                elif request.form["code_duration_number"] == "":
                    feedback = "You need to specify a duration value"
                elif request.form["code_duration_type"] == "":
                    feedback = "You need to specify a duration denomination"

                if len(feedback) > 0:
                    return render_template('generate_access_code/generate_code_2_details.html', user=user,
                                           code_to_use=access_code, orgs=orgs, feedback=feedback)
                else:
                    access_code.access_for_org = return_specific_org_from_list(orgs, int(request.form["org"]))
                    access_code.duration_time = int(request.form["code_duration_number"])
                    access_code.duration_denominator = request.form["code_duration_type"]
                    return redirect(url_for('generate_code_confirm_access_details'))
            else:
                feedback = "You need to select the organisation and duration."
                return render_template('generate_access_code/generate_code_2_details.html', user=user,
                                       code_to_use=access_code, orgs=orgs, feedback=feedback)
    else:
        return redirect(url_for('index'))


@app.route('/generate_access_code_3', methods=['GET', 'POST'])
def generate_code_confirm_access_details():
    global access_code, user, incrementer_access_code, success_message

    if user.logged_in:
        if request.method == 'GET':
            logger.log_benchmark("Generate Access Code (Page 3 - Confirm Details)")
            return render_template('generate_access_code/generate_code_3_confirm_details.html', user=user,
                                   code_to_use=access_code)
        elif request.method == 'POST':
            if len(request.form) > 0:
                if request.form["code_agreement"] == "on":
                    incrementer_access_code += 1
                    access_code.code_id = incrementer_access_code
                    access_code.generate_expiry_from_duration()
                    access_code.generated_code = generate_unique_access_code()
                    access_code.accessed_state = AccessStates.ACTIVE
                    access_code.added_datetime = datetime.datetime.now()
                    user.access_codes.append(access_code)
                    success_message = "The code was successfully generated!"
                    # access_code = AccessCode()
                    logger.log_benchmark("Generate Access Code (Finish)")
                    return redirect(url_for('manage_access_code', code_to_retrieve=access_code.code_id))
                else:
                    feedback = "You need to confirm the access code details to generate."
                    return render_template('generate_access_code/generate_code_3_confirm_details.html', user=user,
                                           code_to_use=access_code, feedback=feedback)
            else:
                feedback = "You need to confirm the access code details to generate."
                return render_template('generate_access_code/generate_code_3_confirm_details.html', user=user,
                                       code_to_use=access_code, feedback=feedback)
    else:
        return redirect(url_for('index'))


# Manage Access Codes Processes


@app.route('/manage_code/<code_to_retrieve>')
def manage_access_code(code_to_retrieve):
    global user, success_message

    if user.logged_in:
        code_to_manage = None
        success_to_display = success_message
        if success_message is not None:
            success_message = None

        for code in user.access_codes:
            if code.code_id == int(code_to_retrieve):
                code_to_manage = code
                break

        if code_to_manage is not None:
            return render_template('manage_access_code/manage_code.html', user=user, code_to_use=code_to_manage,
                                   success=success_to_display)
        else:
            return redirect(url_for('manage_all_access_codes'))
    else:
        return redirect(url_for('index'))


@app.route('/manage_all_codes')
def manage_all_access_codes():
    if user.logged_in:
        return render_template('manage_access_code/manage_all_codes.html', user=user)
    else:
        return redirect(url_for('index'))


# Errors


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', user=user, err=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', user=user, err=error)
