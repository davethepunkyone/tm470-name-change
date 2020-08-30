import os

from flask import render_template, redirect, url_for, request
from app import app
import datetime

import globals.mock_variables as mock
import globals.global_variables as gv
import functions.general_functions as gen_functions

from classes.user_class import User
from classes.signup_verification_class import SignupVerification
from classes.document_class import Document
from classes.marriagecertificate_class import MarriageCertificate
from classes.deedpoll_class import DeedPoll
from classes.decreeabsolute_class import DecreeAbsolute
from classes.accesscode_class import AccessCode
from classes.address_class import Address
from classes.enums import VerifiedStates, AccessStates
from functions.org_functions import return_specific_org_from_list
from functions.access_code_functions import generate_unique_access_code, check_expiry_date_is_valid
from functions.signup_functions import generate_signup_code, email_user_notepad_version, generate_capcha_code, \
    confirm_email_address_value, confirm_password_value
from functions.file_upload_functions import check_filetype_valid, get_upload_directory, return_filename

from functions import logging_functions as logger

# App Config
app.config['UPLOAD_DIRECTORY'] = get_upload_directory()

# Global Lists
users_list = mock.mock_list_of_users()
orgs = mock.mock_list_of_organisations()
orgs.sort(key=lambda org: org.org_name, reverse=False)
signup_verification_list = []

# Global Instances
user = User()
document = Document()
access_code = AccessCode()
capcha_on_page = None

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
    """This covers handling of the initial index page, either loading or submitting the page.

    Allowed methods: GET, POST."""
    global user, failure_message
    if user.logged_in:
        # If the user is already logged in, direct them to their account homepage
        return redirect(url_for('account_home'))
    else:
        if request.method == 'GET':
            # If the page is just loaded, render the page with any applicable feedback messages displayed
            logger.log_benchmark("Load Homepage")
            feedback = failure_message
            failure_message = None
            return render_template('index.html', user=user, feedback=feedback)
        elif request.method == 'POST':
            # Submit the login form and verify the details before logging in
            logger.log_benchmark("Homepage - Attempt Login")
            if len(request.form) > 0:
                email = request.form["email_address"]
                pwd = request.form["password"]
                if email == "" or pwd == "":
                    # Both fields need values to proceed - fail with error advising of this
                    feedback = "You need to provide your email and password to log in."
                    return render_template('index.html', user=user, feedback=feedback)
                else:
                    try:
                        # Attempt to set the user object with the details provided
                        user = return_logged_in_user(email, pwd)
                    except LookupError as err:
                        # If lookup fails, catch the error and return feedback stating failure
                        feedback = err
                        return render_template('index.html', user=user, feedback=feedback)
                    if not user.verified_state:
                        # If the user account is not verified but exists, redirect to page to generate email
                        # activation link
                        return redirect(url_for('new_account_click_link'))
                    else:
                        # Log the user in and direct them to the account homepage
                        user.logged_in = True
                        logger.log_benchmark("Homepage - Successful Login")
                        return redirect(url_for('account_home'))
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to provide your email and password to log in."
                return render_template('index.html', user=user, feedback=feedback)


def return_logged_in_user(email: str, pwd: str) -> User:
    """This function checks the email and password against the global user list and returns a User object if found,
    or raises a LookupError if not found.  If the user is found but the password doesn't match, a LookupError is also
    raised.

    Keyword arguments:
    email (str) -- The email address of the user.
    pwd (str) -- The prototype password of the user."""
    for user_check in users_list:
        if user_check.email == email:
            if user_check.prototype_password == pwd:
                return user_check
            else:
                raise LookupError("The password for the user is not correct.")
    else:
        raise LookupError("The email address specified is not registered with this service.")


@app.route('/forgotten_password')
def forgot_password():
    """This covers rendering the forgotten password page, which is a placeholder document in this prototype."""
    return render_template('forgotten_password.html', user=user)


@app.route('/test/<test_conditions>')
def test(test_conditions):
    """This is a test method used to automatically log in as a mock test user.

    Keyword arguments:
    test_conditions (str) -- The condition to apply."""
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
    """This covers rendering the about page, which is a placeholder document in this prototype."""
    return render_template('general/about.html', user=user)


@app.route('/how_it_works')
def how_it_works():
    """This covers rendering the how it works page, which is a placeholder document in this prototype."""
    return render_template('general/how_it_works.html', user=user)


@app.route('/faq')
def faq():
    """This covers rendering the FAQ page, which is a placeholder document in this prototype."""
    return render_template('general/faq.html', user=user)


@app.route('/contact')
def contact():
    """This covers rendering the contact page, which is a placeholder document in this prototype."""
    return render_template('general/contact.html', user=user)


# New Account Processes


@app.route('/new_account_signup', methods=['GET', 'POST'])
def new_account_signup():
    """This covers handling of the new account signup page, either loading or submitting the page.

    Allowed methods: GET, POST."""
    global user, incrementer_user, capcha_on_page

    if user.logged_in:
        # If the user is already logged in, direct them to their account homepage
        return redirect(url_for('account_home'))
    else:
        if request.method == 'GET':
            # If the page is just loaded, render the page with newly generated CAPCHA displayed
            logger.log_benchmark("New Account Signup - Load Page")
            capcha_on_page = generate_capcha_code()
            return render_template('new_account/new_account_signup.html', user=user, capcha=capcha_on_page)
        elif request.method == 'POST':
            # Submit the login form and verify the details before proceeding
            logger.log_benchmark("New Account Signup - Submit Form")
            if len(request.form) > 0:
                # Form data we may want to pass back in event of error
                form_data = {"forenames": request.form["forenames"],
                             "surname": request.form["surname"],
                             "email": request.form["email"],
                             "email_confirm": request.form["email_confirm"]}
                # Form data we do not want to pass back due to security concerns
                secure_form_data = {"pwd": request.form["password"],
                                    "pwd_confirm": request.form["password_confirm"],
                                    "capcha": request.form["capcha"]}
                initial_feedback = check_new_user_form_values(form_data, secure_form_data)  # Check values
                capcha_on_page = generate_capcha_code()  # Regenerates CAPCHA in event of any type of fail
                if initial_feedback is not None:
                    # Issues with the data have been found so notify the user
                    feedback = initial_feedback
                    return render_template('new_account/new_account_signup.html', user=user, capcha=capcha_on_page,
                                           feedback=feedback, form_data=form_data)
                if not request.form.__contains__("agreement"):
                    # The terms and conditions box has not been confirmed, so notify the user
                    feedback = "You must agree to the terms and conditions to proceed."
                    return render_template('new_account/new_account_signup.html', user=user, capcha=capcha_on_page,
                                           feedback=feedback, form_data=form_data)
                else:
                    # Populate the user object with form data and add to the users list
                    user = User(user_id=incrementer_user, forenames=form_data["forenames"],
                                surname=form_data["surname"], email=form_data["email"],
                                prototype_password=secure_form_data["pwd"], verified_state=False)
                    users_list.append(user)
                    incrementer_user += 1  # Increment global incrementer by 1
                    # Add entry to the signup details global table ready to use
                    signup_details = SignupVerification(signup_code=generate_signup_code(), user_id=user.user_id)
                    signup_verification_list.append(signup_details)
                    # Email the user with their signup link and redirect to page explaining process
                    logger.log_benchmark("New Account Signup - Generate Email Verification")
                    email_user_notepad_version(user, signup_details)
                    return redirect(url_for('new_account_click_link'))
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to complete all the fields to create a new account."
                capcha_on_page = generate_capcha_code()
                return render_template('new_account/new_account_signup.html', user=user, capcha=capcha_on_page,
                                       feedback=feedback)


def check_new_user_form_values(form_data: dict, secure_form_data: dict):
    """This function checks that the values provided on the form meet some minimum requirements before proceeding.
    Returns a string if an issue is found, or None if all requirements are met.

    Keyword arguments:
    form_data (dict) -- Form data that for the purposes of this prototype only are considered normal data.
    secure_form_data (dict) -- Form data that for the purposes of this prototype only are considered secure data."""

    # Check password meets minimum requirements and sets variable if not
    pw_check = confirm_password_value(secure_form_data["pwd"])

    # Check none of the fields requiring text are empty
    if form_data["forenames"] == "" or form_data["surname"] == "" or form_data["email"] == "" or \
            form_data["email_confirm"] == "" or secure_form_data["pwd"] == "" or \
            secure_form_data["pwd_confirm"] == "" or secure_form_data["capcha"] == "":
        return "You need to complete all the fields to create a new account."
    # Check an email account doesn't already exist in the user table for this user
    elif check_user_already_exists(form_data["email"]):
        return "The email address provided is already registered on this service."
    # Check the email address and the confirm email address values match
    elif form_data["email"] != form_data["email_confirm"]:
        return "The email address and confirm email address do not match."
    # Check the email address is in a valid format
    elif not confirm_email_address_value(form_data["email"]):
        return "The email address is not in a valid format."
    # Check password meets minimum requirements (checks above take priority)
    elif pw_check is not None:
        return pw_check
    # Check the password and confirm password values match
    elif secure_form_data["pwd"] != secure_form_data["pwd_confirm"]:
        return "The password and confirm password do not match."
    # Check the CAPCHA value provided matches the value generated
    elif capcha_on_page != secure_form_data["capcha"]:
        return "The CAPCHA verification failed, please try again."
    # All requirements passed
    else:
        return None


def check_user_already_exists(email: str) -> bool:
    """This function checks if the users email address provided already exists in the user table and returns a bool:
    True if yes, False if no.

    Keyword arguments:
    email (str) -- The email address to check in the list."""
    email_present = False
    for user_check in users_list:
        if user_check.email == email:
            email_present = True
            break
    return email_present


@app.route('/new_account_click_link')
def new_account_click_link():
    """This covers rendering the new account verification (click link in email) notification page."""
    global success_message

    if user.logged_in:
        # If the user is already logged in, direct them to their account homepage
        return redirect(url_for('account_home'))
    else:
        # Render the page, displaying the global success message as feedback if applicable
        feedback = success_message
        success_message = None
        logger.log_benchmark("New Account Signup - Email Notification Page Displayed")
        return render_template('new_account/new_account_signup_clicklink.html', user=user, feedback=feedback)


@app.route('/resend_account_email')
def resend_new_account_email():
    """This covers resending the account verification email if the user requests it."""
    global success_message

    if user.logged_in:
        # If the user is already logged in, direct them to their account homepage
        return redirect(url_for('account_home'))
    else:
        # Check the signup user list and resend the email to the specified user, populating the global success
        # message and rendering the new account verification (click link in email) notification page
        for signup_user in signup_verification_list:
            if signup_user.user_id == user.user_id:
                signup_details = signup_user
                email_user_notepad_version(user, signup_details)
                success_message = "Email has been resent."
                logger.log_benchmark("New Account Signup - Email Notification Resent")
                return redirect(url_for('new_account_click_link'))
        else:
            # If the user cannot be found, redirect back to the index page
            return redirect(url_for('index'))


@app.route('/new_account_confirm/<confirm_code>')
def new_account_confirm_code(confirm_code):
    """This covers verifying a user email account by navigating to the link provided within the system generated
    email.

    Keyword arguments:
    confirm_code (str) -- The code associated with the user in the signup verification list."""
    global user, signup_verification_list, failure_message

    # Find the code in the signup verification list and mark the user as verified, before logging them in
    for signup_user in signup_verification_list:
        if signup_user.signup_code == confirm_code:
            user = retrieve_user_from_list(signup_user.user_id)
            user.verified_state = True
            user.logged_in = True
            signup_verification_list.remove(signup_user)
            logger.log_benchmark("New Account Signup - Email Link Confirmed")
            return redirect(url_for('account_home'))
    else:
        # The code isn't found in the table so redirects to the index page with a failure message
        failure_message = "The code provided in the link clicked is not valid."
        return redirect(url_for('index'))


def retrieve_user_from_list(user_id: int) -> User:
    """This function retrieves a specific user using their id from the global users list and returns as a user object.
    Raises a lookup error in the event the user id specified is not found.

    Keyword arguments:
    user_id (int) -- The id of the user in the list of users to retrieve."""
    global users_list

    for user_in_list in users_list:
        if user_in_list.user_id == user_id:
            return user_in_list
    else:
        raise LookupError("The user being queried is not in the list.")


# Existing Account Processes


@app.route('/account')
def account_home():
    """This covers navigating to the users account homepage."""
    if not user.logged_in:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))
    else:
        # Grab the values needed to populate the table on the homepage, and put these in a list of dict objects
        # ready to iterate through
        logger.log_benchmark("Account Homepage")
        table_values = []

        for doc in user.docs:
            total_codes = 0  # Total codes generated by user
            active_codes = 0  # Total codes for user currently listed as active
            expired_codes = 0  # Total codes for user currently listed as expired
            for code in user.access_codes:
                if code.uploaded_document.document_id == doc.document_id:
                    total_codes = + 1
                    if code.accessed_state == AccessStates.ACTIVE:
                        active_codes = + 1
                    elif code.accessed_state == AccessStates.EXPIRED:
                        expired_codes = + 1

            # Create row dict object ready to add to the list
            table_row = {"doc_name": doc.doc_type_with_date,
                         "doc_state": doc.document_verified_state,
                         "total_codes": total_codes,
                         "active_codes": active_codes,
                         "expired_codes": expired_codes}

            table_values.append(table_row)  # Add to list of rows

        return render_template('account_home.html', user=user, table_data=table_values)


@app.route('/edit_profile')
def edit_profile():
    """This covers rendering the contact page, which is a placeholder document in this prototype."""
    if not user.logged_in:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))
    else:
        # Render the edit profile page
        return render_template('profile/edit_profile.html', user=user)


@app.route('/logout')
def logout():
    """This logs the user out and redirects them to the index page."""
    global user
    user.logged_in = False
    user = User()  # Set to blank user object
    logger.log_benchmark("User Logout")
    return redirect(url_for('index'))


# New Document Processes


@app.route('/new_document_1', methods=['GET', 'POST'])
def new_document_selection():
    """This covers handling page 1 of the new document process, either loading or submitting the page.
    This is where the user selects which type of document they are planning to upload.

    Allowed methods: GET, POST."""
    global document, incrementer_document

    if user.logged_in:
        # Firstly check if the user already has a marriage certificate associated with them, as this enables the
        # Decree Absolute option to be selected if true
        marriage_cert_present = False
        for user_doc in user.docs:
            if user_doc.document_type == "Marriage Certificate":
                marriage_cert_present = True

        if request.method == 'GET':
            # If the page is just loaded, render the page with any applicable feedback messages displayed
            logger.log_benchmark("Add New Document - Load Document Type Selection")
            return render_template('add_document/add_doc_1_selection.html', user=user, divorce_on=marriage_cert_present)
        elif request.method == 'POST':
            # If the form is submitted, check the option the user has selected
            if len(request.form) > 0:
                access_code_id_doc = request.form["doc_type"]
                # If Marriage Certificate, set document global to MarriageCertificate object and direct to step 2
                if access_code_id_doc == "marriage_cert":
                    document = MarriageCertificate(document_id=incrementer_document, user_id=user.user_id,
                                                   complete=False)
                    incrementer_document += 1
                    logger.log_benchmark("Add New Document - Select Document Type: Marriage Certificate")
                    return redirect(url_for('new_document_upload_image'))
                # If Deed Poll, set document global to DeedPoll object and direct to step 2
                elif access_code_id_doc == "deed_poll":
                    document = DeedPoll(document_id=incrementer_document, user_id=user.user_id, complete=False)
                    incrementer_document += 1
                    logger.log_benchmark("Add New Document - Select Document Type: Deed Poll")
                    return redirect(url_for('new_document_upload_image'))
                # If Decree Absolute, set document global to DecreeAbsolute object and direct to step 1a
                elif access_code_id_doc == "decree_absolute":
                    document = DecreeAbsolute(document_id=incrementer_document, user_id=user.user_id, complete=False)
                    incrementer_document += 1
                    logger.log_benchmark("Add New Document - Select Document Type: Decree Absolute")
                    return redirect(url_for('new_document_decree_absolute_certificate'))
                else:
                    # The form is empty, so notify the user they have to provide some values before submitting
                    feedback = "You need to select a valid option to proceed."
                    return render_template('add_document/add_doc_1_selection.html', user=user,
                                           divorce_on=marriage_cert_present, feedback=feedback)
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to select an option to proceed."
                return render_template('add_document/add_doc_1_selection.html', user=user,
                                       divorce_on=marriage_cert_present, feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/new_document_1a', methods=['GET', 'POST'])
def new_document_decree_absolute_certificate():
    """This covers handling page 1a of the new document process, either loading or submitting the page.
    This page is only displayed if the user selected Decree Absolute on page 1, as it prompts them to select
    the applicable Marriage Certificate that needs to be applied to this document.

    Allowed methods: GET, POST."""
    global document

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page with any applicable feedback messages displayed
            logger.log_benchmark("Add New Document - Decree Absolute Select Marriage Certificate")
            return render_template('add_document/add_doc_1a_decree_absolute_selection.html', user=user,
                                   doc=document)
        elif request.method == 'POST':
            if len(request.form) > 0:
                # Apply the MarriageCertificate to the DecreeAbsolute and direct to page 2
                marriage_cert_details = request.form["marriage_cert"]
                document.marriage_certificate_details = user.get_specific_listed_doc(int(marriage_cert_details))
                logger.log_benchmark("Add New Document - Decree Absolute Marriage Certificate Selected")
                return redirect(url_for('new_document_upload_image'))
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to select at least one option."
                return render_template('add_document/add_doc_1a_decree_absolute_selection.html', user=user,
                                       doc=document, feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/new_document_2', methods=['GET', 'POST'])
def new_document_upload_image():
    """This covers handling page 2 of the new document process, either loading or submitting the page.
    This page is used to upload a copy of the image being used for this document.

    Allowed methods: GET, POST."""
    global document

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page
            logger.log_benchmark("Add New Document - Image Upload")
            return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document)
        if request.method == 'POST':
            # This checks that the user has actually specified a file to be uploaded
            if 'user_file' not in request.files:
                # File upload control has not been initialized
                if document.uploaded_file_path is not None:
                    # If there's no uploaded document on the page but an image has been uploaded previously (e.g. the
                    # user navigated back to this page) then let the user move back to page 3
                    logger.log_benchmark("Add New Document - Image Upload (Bypass)")
                    return redirect(url_for('new_document_confirm_image'))
                else:
                    # No file has been uploaded so notify the user they have to upload a file before proceeding
                    feedback = "No file was uploaded."
                    return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document,
                                           feedback=feedback)
            else:
                # File upload control has been initialized
                file_to_use = request.files["user_file"]
                if file_to_use.filename == "" and document.uploaded_file_path is not None:
                    # If there's no uploaded document on the page but an image has been uploaded previously (e.g. the
                    # user navigated back to this page) then let the user move back to page 3
                    logger.log_benchmark("Add New Document - Image Upload (Bypass)")
                    return redirect(url_for('new_document_confirm_image'))
                elif file_to_use.filename == "" and document.uploaded_file_path is None:
                    # No file has been uploaded and a file doesn't already exist so notify the user they have to upload
                    # a file before proceeding
                    feedback = "No file was uploaded."
                    return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document,
                                           feedback=feedback)

                # Check that the filetype provided is valid, before uploading the file into the uploads directory
                # with a filename specific to the user.  Once complete redirect the user to page 3
                if check_filetype_valid(file_to_use.filename):
                    filename = return_filename(document, file_to_use.filename)
                    filepath = os.path.join(app.config['UPLOAD_DIRECTORY'], filename)
                    file_to_use.save(filepath)
                    document.uploaded_file_path = filename
                    logger.log_benchmark("Add New Document - Image Upload Processed")
                    return redirect(url_for('new_document_confirm_image'))
                else:
                    # The filetype provided isn't valid, so notify the user accordingly
                    feedback = "The filetype provided is invalid."
                    return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document,
                                           feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/new_document_3', methods=['GET', 'POST'])
def new_document_confirm_image():
    """This covers handling page 3 of the new document process, either loading or submitting the page.
    This page is used to confirm the uploaded image is good before proceeding.

    Allowed methods: GET, POST."""

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page.
            logger.log_benchmark("Add New Document - Image Confirm")
            return render_template('add_document/add_doc_3_confirm_image.html', user=user, doc=document)
        if request.method == 'POST':
            if len(request.form) > 0:
                if request.form["image_correct"] == "on":
                    # Confirmation received that the image is correct, so redirect to page 4
                    logger.log_benchmark("Add New Document - Image Confirmed Correct")
                    return redirect(url_for('new_document_add_personal_details'))
                else:
                    # The form is empty, so notify the user they have to confirm the image is correct before submitting
                    feedback = "You need to confirm the image has uploaded correctly."
                    return render_template('add_document/add_doc_3_confirm_image.html', user=user, doc=document,
                                           feedback=feedback)
            else:
                # The form is empty, so notify the user they have to confirm the image is correct before submitting
                feedback = "You need to confirm the image has uploaded correctly."
                return render_template('add_document/add_doc_3_confirm_image.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/new_document_4', methods=['GET', 'POST'])
def new_document_add_personal_details():
    """This covers handling page 4 of the new document process, either loading or submitting the page.
    This page is used to take the personal details of the user applicable to the document.

    Allowed methods: GET, POST."""
    global document

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page
            logger.log_benchmark("Add New Document - Personal Details Load")
            return render_template('add_document/add_doc_4_add_personal_details.html', user=user, doc=document)
        elif request.method == 'POST':
            # When the form is submitted, populate all the form elements meet the minimum criteria
            if len(request.form) > 0:
                form_data = {"prev_forenames": request.form["prev_forenames"],
                             "prev_surname": request.form["prev_surname"],
                             "forenames": request.form["forenames"],
                             "surname": request.form["surname"],
                             "address_house_name_no": request.form["address_name_no"],
                             "address_line_1": request.form["address_line_1"],
                             "address_line_2": request.form["address_line_2"],
                             "address_city": request.form["address_town_city"],
                             "address_postcode": request.form["address_postcode"]}

                initial_feedback = check_personal_details(form_data)
                if initial_feedback is not None:
                    # Render the page with a message to the user explaining the issue with their data.
                    return render_template('add_document/add_doc_4_add_personal_details.html', user=user, doc=document,
                                           feedback=initial_feedback, form_data=form_data)
                else:
                    # Populate the user personal details in the document object and redirect to page 5.
                    document.old_forenames = form_data["prev_forenames"]
                    document.old_surname = form_data["prev_surname"]
                    document.new_forenames = form_data["forenames"]
                    document.new_surname = form_data["surname"]
                    document.address = Address(house_name_no=form_data["address_house_name_no"],
                                               line_1=form_data["address_line_1"], line_2=form_data["address_line_2"],
                                               town_city=form_data["address_city"],
                                               postcode=form_data["address_postcode"])
                    logger.log_benchmark("Add New Document - Personal Details Added")
                    return redirect(url_for('new_document_confirm_personal_details'))
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to complete the mandatory fields to proceed."
                return render_template('add_document/add_doc_4_add_personal_details.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


def check_personal_details(form_data: dict) -> str or None:
    """This function checks the personal form details meet the minimum requirements. Returns a str if requirements
    are not met, or None if all requirements are met.

    Keyword arguments:
    form_data (dict) -- The details provided on the personal details form."""

    # Check all mandatory fields are filled in
    if form_data["address_house_name_no"] == "" or form_data["address_line_1"] == "" or \
            form_data["address_city"] == "" or form_data["address_postcode"] == "":
        return "The mandatory address fields have not been populated."
    # Check the previous forename is not blank and same as the new forename
    elif form_data["prev_forenames"] != "" and form_data["prev_forenames"] == form_data["forenames"]:
        return "The previous forename and new forename cannot be the same."
    # Check the previous surname is not blank and same as the new surname
    elif form_data["prev_surname"] != "" and form_data["prev_surname"] == form_data["surname"]:
        return "The previous surname and new surname cannot be the same."
    # Check the previous forename is blank and the new forename is not blank
    elif form_data["prev_forenames"] == "" and form_data["forenames"] != "":
        return "You cannot specify a new forename(s) value without providing the previous forename(s)."
    # Check the previous surname is blank and the new surname is not blank
    elif form_data["prev_surname"] == "" and form_data["surname"] != "":
        return "You cannot specify a new surname value without providing the previous surname."
    # Check the new forename is blank and the previous forename is not blank
    elif form_data["forenames"] == "" and form_data["prev_forenames"] != "":
        return "You cannot specify a previous forename(s) value without providing the new forename(s)."
    # Check the new surname is blank and the previous surname is not blank
    elif form_data["surname"] == "" and form_data["prev_surname"] != "":
        return "You cannot specify a previous surname value without providing the new surname."
    # All requirements passed
    else:
        return None


@app.route('/new_document_5', methods=['GET', 'POST'])
def new_document_confirm_personal_details():
    """This covers handling page 5 of the new document process, either loading or submitting the page.
    This page is used to confirm the personal details of the user applicable to the document.

    Allowed methods: GET, POST."""
    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page
            logger.log_benchmark("Add New Document - Personal Details Confirm Loaded")
            return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user, doc=document)
        elif request.method == 'POST':
            # Check that the user has confirmed the details and if they have, redirect to page 6.
            if len(request.form) > 0:
                if request.form["personal_details_correct"] == "on":
                    logger.log_benchmark("Add New Document - Personal Details Confirmed")
                    return redirect(url_for('new_document_add_document_details'))
                else:
                    # The form is empty, so notify the user they have to provide some values before submitting
                    feedback = "You need to confirm the details provided are correct."
                    return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user,
                                           doc=document, feedback=feedback)
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to confirm the details provided are correct."
                return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/new_document_6', methods=['GET', 'POST'])
def new_document_add_document_details():
    """This covers handling page 6 of the new document process, either loading or submitting the page.
    This page is used to confirm the specific document details applicable to the document.

    Allowed methods: GET, POST."""
    global document

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page
            logger.log_benchmark("Add New Document - Document Details Load")
            return render_template('add_document/add_doc_6_add_document_details.html', user=user, doc=document)
        elif request.method == 'POST':
            # This checks and populates the global document dependant on the document type
            if len(request.form) > 0:
                if document.document_type == "Marriage Certificate":
                    # Puts all marriage related items in a form and checks for feedback
                    marriage_obj = {"marriage_day": request.form["marriage_date_day"],
                                    "marriage_month": request.form["marriage_date_month"],
                                    "marriage_year": request.form["marriage_date_year"],
                                    "marriage_age": request.form["marriage_age_cert"],
                                    "marriage_reg_district": request.form["marriage_reg_district"],
                                    "marriage_no": request.form["marriage_no"]}
                    initial_feedback = check_doc_details_mandatory_fields(marriage_obj)

                    if initial_feedback is not None:
                        # Notify the user that there is an issue with the marriage data provided
                        return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                               doc=document, feedback=initial_feedback, form_data=marriage_obj)
                    else:
                        date_to_use = datetime.date(int(marriage_obj["marriage_year"]),
                                                    int(marriage_obj["marriage_month"]),
                                                    int(marriage_obj["marriage_day"]))

                        # Check that a Marriage Certificate for this date doesn't already exist for this user
                        secondary_feedback = check_doc_details_dont_already_exist_for_user(date_to_use)
                        if secondary_feedback is not None:
                            # Notify the user they already have a Marriage Certificate with this date registered
                            return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                                   doc=document, feedback=secondary_feedback,
                                                   form_data=marriage_obj)

                        # Populate the Marriage Certificate with form data and redirect to page 7
                        document.change_of_name_date = date_to_use
                        document.age_on_certificate = int(marriage_obj["marriage_age"])
                        document.registration_district = marriage_obj["marriage_reg_district"]
                        document.marriage_number = int(marriage_obj["marriage_no"])

                        logger.log_benchmark("Add New Document - Document Details Added (Marriage Certificate)")
                        return redirect(url_for('new_document_confirm_document_details'))

                elif document.document_type == "Deed Poll":
                    # Puts all deed poll related items in a form and checks for feedback
                    deed_poll_obj = {"deed_date_day": request.form["deed_date_day"],
                                     "deed_date_month": request.form["deed_date_month"],
                                     "deed_date_year": request.form["deed_date_year"]}
                    # Specific handling for radio buttons if none are selected
                    if "deed_registered" in request.form:
                        deed_poll_obj.update({"deed_registered": request.form["deed_registered"]})
                    else:
                        deed_poll_obj.update({"deed_registered": None})

                    initial_feedback = check_doc_details_mandatory_fields(deed_poll_obj)

                    if initial_feedback is not None:
                        # Notify the user that there is an issue with the deed poll data provided
                        return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                               doc=document, feedback=initial_feedback, form_data=deed_poll_obj)
                    else:
                        date_to_use = datetime.date(int(deed_poll_obj["deed_date_year"]),
                                                    int(deed_poll_obj["deed_date_month"]),
                                                    int(deed_poll_obj["deed_date_day"]))

                        # Check that a Deed Poll for this date doesn't already exist for this user
                        secondary_feedback = check_doc_details_dont_already_exist_for_user(date_to_use)
                        if secondary_feedback is not None:
                            # Notify the user they already have a Deed Poll with this date registered
                            return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                                   doc=document, feedback=secondary_feedback,
                                                   form_data=deed_poll_obj)

                        # Populate the Deed Poll with form data and redirect to page 7
                        document.change_of_name_date = date_to_use
                        document.registered_with_courts = gen_functions.yesno_to_bool(request.form["deed_registered"])

                        logger.log_benchmark("Add New Document - Document Details Added (Deed Poll)")
                        return redirect(url_for('new_document_confirm_document_details'))

                elif document.document_type == "Decree Absolute":
                    # Puts all decree absolute related items in a form and checks for feedback
                    decree_absolute_obj = {"decree_date_day": request.form["decree_date_day"],
                                           "decree_date_month": request.form["decree_date_month"],
                                           "decree_date_year": request.form["decree_date_year"],
                                           "decree_issuing_court": request.form["decree_issuing_court"],
                                           "decree_no_of_matter": request.form["decree_no_of_matter"]}
                    initial_feedback = check_doc_details_mandatory_fields(decree_absolute_obj)

                    if initial_feedback is not None:
                        # Notify the user that there is an issue with the decree absolute data provided
                        return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                               doc=document, feedback=initial_feedback, form_data=decree_absolute_obj)
                    else:
                        date_to_use = datetime.date(int(decree_absolute_obj["decree_date_year"]),
                                                    int(decree_absolute_obj["decree_date_month"]),
                                                    int(decree_absolute_obj["decree_date_day"]))

                        # Check that a Decree Absolute for this date doesn't already exist for this user
                        secondary_feedback = check_doc_details_dont_already_exist_for_user(date_to_use)
                        if secondary_feedback is not None:
                            # Notify the user they already have a Decree Absolute with this date registered
                            return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                                   doc=document, feedback=secondary_feedback,
                                                   form_data=decree_absolute_obj)

                        # Populate the Decree Absolute with form data and redirect to page 7
                        document.change_of_name_date = date_to_use
                        document.issuing_court = request.form["decree_issuing_court"]
                        document.number_of_matter = request.form["decree_no_of_matter"]

                        logger.log_benchmark("Add New Document - Document Details Added (Decree Absolute)")
                        return redirect(url_for('new_document_confirm_document_details'))

                else:
                    # Something has gone wrong as the document type hasn't been recognised, should not be possible
                    # for this issue to occur but handling it just in case
                    feedback = "Something has gone wrong here as this error shouldn't appear."
                    return render_template('add_document/add_doc_6_add_document_details.html', user=user, doc=document,
                                           feedback=feedback)
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to complete the mandatory fields to proceed."
                return render_template('add_document/add_doc_6_add_document_details.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


def check_doc_details_dont_already_exist_for_user(day_to_check: datetime.date) -> str or None:
    """This function checks if a document of the type being uploaded already exists for the date the user is trying
    to upload for.  If so, returns a str advising of this, otherwise returns None.

    Keyword arguments:
    day_to_check (datetime.date) -- The date of the document that is being added."""
    for check_users_doc in user.docs:
        # Checks the documents in the global user list but does not make any changes
        if document.document_type == check_users_doc.document_type:
            if day_to_check == check_users_doc.change_of_name_date:
                return "A {} for this date ({}) already exists." \
                    .format(check_users_doc.document_type, check_users_doc.change_of_name_date_as_string)
    return None


def check_doc_details_mandatory_fields(fields_to_check: dict) -> str or None:
    """This function checks that all the mandatory information has been provided for the document type being uploaded.
    Returns a str if an issue is detected, or None if all mandatory conditions are met.

    Keyword arguments:
    fields_to_check (dict) -- The document form data."""

    # If the document is a Marriage Certificate
    if document.document_type == "Marriage Certificate":
        # Checks all mandatory fields have been populated
        if fields_to_check["marriage_day"] == "" or fields_to_check["marriage_month"] == "" or \
                fields_to_check["marriage_year"] == "" or fields_to_check["marriage_age"] == "" or \
                fields_to_check["marriage_reg_district"] == "" or fields_to_check["marriage_no"] == "":
            return "All mandatory fields need to be completed to proceed."
        # Checks marriage day is a number value
        elif not fields_to_check["marriage_day"].isnumeric():
            return "The marriage day value must be a number."
        # Checks marriage day value is between 1 and 31
        elif int(fields_to_check["marriage_day"]) > 31 or \
                int(fields_to_check["marriage_day"].isnumeric()) < 1:
            return "The marriage day value is not valid."
        # Checks marriage month is a number value
        elif not fields_to_check["marriage_month"].isnumeric():
            return "The marriage month value must be a number."
        # Checks marriage month value is between 1 and 12
        elif int(fields_to_check["marriage_month"]) > 12 or \
                int(fields_to_check["marriage_month"]) < 1:
            return "The marriage month value is not valid."
        # Checks marriage year is a number value
        elif not fields_to_check["marriage_year"].isnumeric():
            return "The marriage year value must be a number."
        # Checks marriage year value is between 1900 and the current year
        elif int(fields_to_check["marriage_year"]) > datetime.datetime.now().year or \
                int(fields_to_check["marriage_year"]) < 1900:
            return "The marriage year value is not valid."
        # Checks marriage age is a number value
        elif not fields_to_check["marriage_age"].isnumeric():
            return "The marriage age value must be a number."
        # Checks marriage age is between the globally defined minimum and maximum allowed ages
        elif int(fields_to_check["marriage_age"]) > gv.maximum_age_marriage or \
                int(fields_to_check["marriage_age"]) < gv.minimum_age_marriage:
            return "The marriage age value is not valid."
        # Checks marriage number is a number value
        elif not fields_to_check["marriage_no"].isnumeric():
            return "The marriage number value must be a number."
        # Checks marriage number is not less than 1
        elif int(fields_to_check["marriage_no"]) < 1:
            return "The marriage number value is not valid."
        # All mandatory conditions met
        else:
            return None
    # If the document is a Deed Poll
    elif document.document_type == "Deed Poll":
        # Checks all mandatory fields have been populated
        if fields_to_check["deed_date_day"] == "" or fields_to_check["deed_date_month"] == "" or \
                fields_to_check["deed_date_year"] == "" or fields_to_check["deed_registered"] == "":
            return "All mandatory fields need to be completed to proceed."
        # Checks deed day is a number value
        elif not fields_to_check["deed_date_day"].isnumeric():
            return "The deed poll day value must be a number."
        # Checks deed day value is between 1 and 31
        elif int(fields_to_check["deed_date_day"]) > 31 or \
                int(fields_to_check["deed_date_day"].isnumeric()) < 1:
            return "The deed poll day value is not valid."
        # Checks deed month is a number value
        elif not fields_to_check["deed_date_month"].isnumeric():
            return "The deed poll month value must be a number."
        # Checks deed month value is between 1 and 12
        elif int(fields_to_check["deed_date_month"]) > 12 or \
                int(fields_to_check["deed_date_month"]) < 1:
            return "The deed poll month value is not valid."
        # Checks deed year is a number value
        elif not fields_to_check["deed_date_year"].isnumeric():
            return "The deed poll year value must be a number."
        # Checks deed year value is between 1900 and the current year
        elif int(fields_to_check["deed_date_year"]) > datetime.datetime.now().year or \
                int(fields_to_check["deed_date_year"]) < 1900:
            return "The deed poll year value is not valid."
        # Checks deed registered has been set
        elif fields_to_check["deed_registered"] is None:
            return "You must select if the document has been registered with the courts or not."
        # All mandatory conditions met
        else:
            return None
    # If the document is a Decree Absolute
    elif document.document_type == "Decree Absolute":
        # Checks all mandatory fields have been populated
        if fields_to_check["decree_date_day"] == "" or fields_to_check["decree_date_month"] == "" or \
                fields_to_check["decree_date_year"] == "" or fields_to_check["decree_issuing_court"] == "" or \
                fields_to_check["decree_no_of_matter"] == "":
            return "All mandatory fields need to be completed to proceed."
        # Checks decree day is a number value
        elif not fields_to_check["decree_date_day"].isnumeric():
            return "The decree absolute day value must be a number."
        # Checks decree day value is between 1 and 31
        elif int(fields_to_check["decree_date_day"]) > 31 or \
                int(fields_to_check["decree_date_day"].isnumeric()) < 1:
            return "The decree absolute day value is not valid."
        # Checks decree month is a number value
        elif not fields_to_check["decree_date_month"].isnumeric():
            return "The decree absolute month value must be a number."
        # Checks deed month value is between 1 and 12
        elif int(fields_to_check["decree_date_month"]) > 12 or \
                int(fields_to_check["decree_date_month"]) < 1:
            return "The decree absolute month value is not valid."
        # Checks decree year is a number value
        elif not fields_to_check["decree_date_year"].isnumeric():
            return "The decree absolute year value must be a number."
        # Checks decree year value is between 1900 and the current year
        elif int(fields_to_check["decree_date_year"]) > datetime.datetime.now().year or \
                int(fields_to_check["decree_date_year"]) < 1900:
            return "The decree absolute year value is not valid."
        # Checks decree number of matter is a number value
        elif not fields_to_check["decree_no_of_matter"].isnumeric():
            return "The number of matter value must be a number."
        # Checks decree day number of matter is not less than 1
        elif int(fields_to_check["decree_no_of_matter"]) < 1:
            return "The number of matter value is not valid."
        # Checks the change of name date on the decree absolute is not before the marriage date on the associated
        # marriage certificate
        elif document.marriage_certificate_details.change_of_name_date >= \
                datetime.date(int(fields_to_check["decree_date_year"]), int(fields_to_check["decree_date_month"]),
                              int(fields_to_check["decree_date_day"])):
            return "The Decree Absolute date cannot be before or on the associated wedding date ({})." \
                .format(document.marriage_certificate_details.change_of_name_date_as_string)
        # All mandatory conditions met
        else:
            return None
    # The document type wasn't recognised and an issue has occurred - this shouldn't happen but handled just in case
    else:
        return "The document type wasn't recognised, this error shouldn't occur."


@app.route('/new_document_7', methods=['GET', 'POST'])
def new_document_confirm_document_details():
    """This covers handling page 7 of the new document process, either loading or submitting the page.
    This page is used to confirm the document details of the document being uploaded.

    Allowed methods: GET, POST."""
    global document, user

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page
            logger.log_benchmark("Add New Document - Document Details Confirm Load")
            return render_template('add_document/add_doc_7_confirm_document_details.html', user=user, doc=document)
        elif request.method == 'POST':
            # If the document details are confirmed, add the details and finish the process
            if len(request.form) > 0:
                if request.form["doc_details_correct"] == "on":
                    # Check that the user hasn't pressed the back button after finishing and tries to add the same
                    # document a second time
                    doc_check_feedback = check_doc_details_dont_already_exist_for_user(document.change_of_name_date)
                    if doc_check_feedback is not None:
                        # Notify user that the document is already present
                        return render_template('add_document/add_doc_7_confirm_document_details.html', user=user,
                                               doc=document, feedback=doc_check_feedback)
                    # Flag the document is now complete
                    document.complete = True
                    # If document is a deed poll that isn't verified with courts, there is no way to validate it
                    if document.document_type == "Deed Poll":
                        if not document.registered_with_courts:
                            document.document_verified_state = VerifiedStates.NOT_APPLICABLE

                    # Add document to the users global document list and redirect to the finish page
                    user.docs.append(document)
                    logger.log_benchmark("Add New Document - Document Details Confirmed")
                    return redirect(url_for('new_document_finish'))
                else:
                    # The form is empty, so notify the user they have to provide some values before submitting
                    feedback = "You need to confirm the details provided are correct."
                    return render_template('add_document/add_doc_7_confirm_document_details.html', user=user,
                                           doc=document, feedback=feedback)
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to confirm the details provided are correct."
                return render_template('add_document/add_doc_7_confirm_document_details.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/new_document_8')
def new_document_finish():
    """This covers handling the finish page of the new document process.  This page is used to notify the user of a
    successful upload and next steps."""
    if user.logged_in:
        logger.log_benchmark("Add New Document - Finish Page Load")
        return render_template('add_document/add_doc_8_finish.html', user=user, doc=document, orgs=orgs)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/verify_document/<code>')
def verify_document(code):
    """This covers the admin page for allowing a document to enter a specific verification state for the purposes of
    the prototype.

    Keyword arguments:
    code (str) -- The enum code to apply to the document."""
    if user.logged_in:
        if code == "0":
            # Default page load - just render the page
            logger.log_benchmark("Admin Action - Load Verify Document")
            return render_template('add_document/document_verification.html', user=user, doc=document)
        elif code == "1":
            # Set to awaiting verification
            document.document_verified_state = VerifiedStates.AWAITING_VERIFICATION
        elif code == "2":
            # Set to verification failed
            document.document_verified_state = VerifiedStates.VERIFICATION_FAILED
            document.document_verified_comment = "Document is not in good enough condition to verify."
        elif code == "9":
            # Set to verified
            document.document_verified_state = VerifiedStates.VERIFIED

        # Sets the verifying org and redirects to account home
        document.document_verified_org = "CYN Auto Admin"
        logger.log_benchmark("Admin Action - Verify Document Action")
        return redirect(url_for('account_home'))
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


# New Document Processes


@app.route('/manage_all_documents')
def manage_all_documents():
    """This covers the manage all documents page to allow users to see all the documents they have uploaded."""
    global success_message

    if user.logged_in:
        # Checks for a success message and renders the page, displaying the message if applicable and clearing the
        # global variable in the process
        success_to_display = success_message
        if success_message is not None:
            success_message = None

        logger.log_benchmark("Manage All Documents")
        return render_template('manage_documents/manage_all_documents.html', user=user, success=success_to_display)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/manage_document/<doc_id>')
def manage_document(doc_id):
    """This covers displaying the details of a specific document the user has uploaded.

    Keyword arguments:
    doc_id (str) -- The id of the document from the global users document list."""
    global document

    if user.logged_in:
        # Use the id to retrieve the document and then populate the page appropriately
        doc_to_manage = None
        for doc_to_check in user.docs:
            if doc_to_check.document_id == int(doc_id):
                doc_to_manage = doc_to_check
                break

        if doc_to_manage is not None:
            logger.log_benchmark("Manage Document Load - " + doc_to_manage.document_type)
            document = doc_to_manage
            return render_template('manage_documents/manage_document.html', user=user, doc=doc_to_manage)
        else:
            # If the document id is not found for the user, return to manage all documents
            return redirect(url_for('manage_all_documents'))
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/view_document_image/<doc_id>')
def view_document_image(doc_id):
    """This covers displaying the image of a specific document the user has uploaded.

    Keyword arguments:
    doc_id (str) -- The id of the document from the global users document list."""
    global document

    if user.logged_in:
        # Use the id to retrieve the document and then populate the page appropriately
        doc_to_manage = None
        for doc_to_check in user.docs:
            if doc_to_check.document_id == int(doc_id):
                doc_to_manage = doc_to_check
                break

        if doc_to_manage is not None:
            logger.log_benchmark("Manage Document View Image Load - " + doc_to_manage.document_type)
            document = doc_to_manage
            return render_template('manage_documents/view_document_image.html', user=user, doc=doc_to_manage)
        else:
            # If the document id is not found for the user, return to manage all documents
            return redirect(url_for('manage_all_documents'))
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/remove_document/<doc_id>', methods=['GET', 'POST'])
def remove_document(doc_id):
    """This covers removing a specific document the user has uploaded.

    Keyword arguments:
    doc_id (str) -- The id of the document from the global users document list."""
    global user, document, success_message

    if user.logged_in:
        doc_to_manage = None
        for doc_to_check in user.docs:
            if doc_to_check.document_id == int(doc_id):
                doc_to_manage = doc_to_check
                break

        if doc_to_manage is not None:
            if request.method == 'GET':
                # If the page is just loaded, render the page
                logger.log_benchmark("Remove Document Load - " + doc_to_manage.document_type)
                return render_template('manage_documents/remove_document.html', user=user, doc=doc_to_manage)
            elif request.method == 'POST':
                # When submitting the form, check confirmation is present and proceed
                if len(request.form) > 0:
                    if request.form["confirm_remove"] == "on":
                        # Stop existing Access Codes from working by changing their state and setting the expiry
                        # datetime to now
                        for codes in user.access_codes:
                            if codes.uploaded_document.document_id == doc_to_manage.document_id:
                                if codes.accessed_state in (AccessStates.ACTIVE, AccessStates.EXPIRED):
                                    codes.accessed_state = AccessStates.DOCUMENT_NO_LONGER_AVAILABLE
                                codes.expiry = datetime.datetime.now()
                        # Remove the document from the global user and redirect to manage all documents with a message
                        # notifying the user that the document has been successfully removed
                        user.docs.remove(doc_to_manage)

                        logger.log_benchmark("Remove Document Confirmed - " + doc_to_manage.document_type)
                        success_message = "The document was successfully removed."
                        return redirect(url_for('manage_all_documents'))
                    else:
                        # The form is empty, so notify the user they have to provide some values before submitting
                        feedback = "You must confirm that you want to remove the document."
                        return render_template('manage_documents/remove_document.html', user=user, doc=doc_to_manage,
                                               feedback=feedback)
                else:
                    # The form is empty, so notify the user they have to provide some values before submitting
                    feedback = "You must confirm that you want to remove the document."
                    return render_template('manage_documents/remove_document.html', user=user, doc=doc_to_manage,
                                           feedback=feedback)
        else:
            # If the document id is not found for the user, return to manage all documents
            return redirect(url_for('manage_all_documents'))
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


# Generate New Access Code Processes


@app.route('/generate_access_code_1', methods=['GET', 'POST'])
def generate_code_document_selection():
    """This covers handling page 1 of the generate access code process, either loading or submitting the page.
    This is where the user selects which document they are generating an access code for.

    Allowed methods: GET, POST."""
    global access_code, user

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, prepare a new access code object and render the page
            logger.log_benchmark("Generate Access Code - Select Document")
            access_code = AccessCode()
            return render_template('generate_access_code/generate_code_1_selection.html', user=user)
        elif request.method == 'POST':
            # Take the document the user has selected and populate the access code object with it ready to use, before
            # redirecting to page 2
            if len(request.form) > 0:
                access_code_id_doc = request.form["user_doc"]
                access_code.uploaded_document = user.get_specific_listed_doc(int(access_code_id_doc))
                logger.log_benchmark("Generate Access Code - Document Selected")
                return redirect(url_for('generate_code_access_details'))
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to select at least one option."
                return render_template('generate_access_code/generate_code_1_selection.html', user=user,
                                       feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/generate_access_code_2', methods=['GET', 'POST'])
def generate_code_access_details():
    """This covers handling page 2 of the generate access code process, either loading or submitting the page.
    This is where the user selects who the access code is for and how long it should be active for.

    Allowed methods: GET, POST."""
    global access_code, user

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page
            logger.log_benchmark("Generate Access Code - Access Details")
            return render_template('generate_access_code/generate_code_2_details.html', user=user,
                                   code_to_use=access_code, orgs=orgs)
        elif request.method == 'POST':
            # Check the details have been provided
            if len(request.form) > 0:
                feedback = None

                # Populate a dict object with the form details
                form_data = {"org": request.form["org"],
                             "code_duration_number": request.form["code_duration_number"],
                             "code_duration_type": request.form["code_duration_type"]}

                # If the form grabbed the id for the org, convert it to an int
                if form_data["org"].isnumeric():
                    form_data.update({"org": int(request.form["org"])})

                # Generate feedback if no org was picked
                if form_data["org"] == "":
                    feedback = "You need to select an organisation."
                # Generate feedback if the code duration is not set
                elif form_data["code_duration_number"] == "":
                    feedback = "You need to specify a duration value."
                # Generate feedback if the code duration is not a number
                elif not form_data["code_duration_number"].isnumeric():
                    feedback = "The duration value must be a number."
                # Generate feedback if the code duration is less than 1
                elif int(form_data["code_duration_number"]) < 1:
                    feedback = "The duration value must be greater than 0."
                # Generate feedback if the code denominator is not in the list
                elif form_data["code_duration_type"] not in ("hours", "days"):
                    feedback = "You need to specify a valid duration denomination."

                if feedback is None:
                    # If no feedback detected yet, check if the org selected requires the document to be verified and
                    # compare against the document selected, generating feedback if the document isn't verified but the
                    # org they have selected needs it to be verified.
                    org_to_check = return_specific_org_from_list(orgs, int(form_data["org"]))
                    if org_to_check.requires_verified and \
                            access_code.uploaded_document.document_verified_state != VerifiedStates.VERIFIED:
                        feedback = "This organisation requires the document to be verified first."

                if feedback is None:
                    # If no feedback detected yet, check the expiry date that would be generated is within the
                    # acceptable date values
                    feedback = check_expiry_date_is_valid(None, int(form_data["code_duration_number"]),
                                                          form_data["code_duration_type"])

                if feedback is not None:
                    # If feedback was generated, notify the user of this feedback
                    return render_template('generate_access_code/generate_code_2_details.html', user=user,
                                           code_to_use=access_code, orgs=orgs, feedback=feedback, form_data=form_data)
                else:
                    # Populate the access code with the applicable details and redirect to page 3
                    access_code.access_for_org = return_specific_org_from_list(orgs, int(form_data["org"]))
                    access_code.duration_time = int(form_data["code_duration_number"])
                    access_code.duration_denominator = form_data["code_duration_type"]
                    logger.log_benchmark("Generate Access Code - Access Details Submitted")
                    return redirect(url_for('generate_code_confirm_access_details'))
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to select the organisation and duration."
                return render_template('generate_access_code/generate_code_2_details.html', user=user,
                                       code_to_use=access_code, orgs=orgs, feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/generate_access_code_3', methods=['GET', 'POST'])
def generate_code_confirm_access_details():
    """This covers handling page 3 of the generate access code process, either loading or submitting the page.
    This is where the user confirms who the access code is for and how long it should be active for.

    Allowed methods: GET, POST."""
    global access_code, user, incrementer_access_code, success_message

    if user.logged_in:
        if request.method == 'GET':
            # If the page is just loaded, render the page
            logger.log_benchmark("Generate Access Code - Access Details Confirm Load")
            return render_template('generate_access_code/generate_code_3_confirm_details.html', user=user,
                                   code_to_use=access_code)
        elif request.method == 'POST':
            # Check the user has confirmed the details are valid
            if len(request.form) > 0:
                if request.form["code_agreement"] == "on":
                    incrementer_access_code += 1  # Increments access code id by 1
                    # Sets the access code details and adds this code to the global user list, along with generating a
                    # success message before redirecting to the manage access code page for the code generated
                    access_code.code_id = incrementer_access_code
                    access_code.generate_expiry_from_duration()
                    access_code.generated_code = generate_unique_access_code()
                    access_code.accessed_state = AccessStates.ACTIVE
                    access_code.added_datetime = datetime.datetime.now()
                    user.access_codes.append(access_code)
                    success_message = "The code was successfully generated!"

                    logger.log_benchmark("Generate Access Code - Access Details Confirmed")
                    return redirect(url_for('manage_access_code', code_to_retrieve=access_code.code_id))
                else:
                    # The form is empty, so notify the user they have to provide some values before submitting
                    feedback = "You need to confirm the access code details to generate."
                    return render_template('generate_access_code/generate_code_3_confirm_details.html', user=user,
                                           code_to_use=access_code, feedback=feedback)
            else:
                # The form is empty, so notify the user they have to provide some values before submitting
                feedback = "You need to confirm the access code details to generate."
                return render_template('generate_access_code/generate_code_3_confirm_details.html', user=user,
                                       code_to_use=access_code, feedback=feedback)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


# Manage Access Codes Processes


@app.route('/manage_code/<code_to_retrieve>')
def manage_access_code(code_to_retrieve):
    """This covers retrieving a specific access code assigned to the user to view and manage.

    Keyword arguments:
    code_to_retrieve (str) -- The id of the access code that needs managing."""
    global user, success_message

    if user.logged_in:
        # Checks if a global success message exists and prepares this for the page specifically and clearing the global
        # variable in the process
        code_to_manage = None
        success_to_display = success_message
        if success_message is not None:
            success_message = None

        # Loop through the access codes and retrieve the desired code before rendering the page
        for code in user.access_codes:
            if code.code_id == int(code_to_retrieve):
                code_to_manage = code
                break

        if code_to_manage is not None:
            logger.log_benchmark("Manage Access Code - " + code_to_manage.uploaded_document.document_type + " for " +
                                 code_to_manage.access_for_org.org_name)
            return render_template('manage_access_code/manage_code.html', user=user, code_to_use=code_to_manage,
                                   success=success_to_display, date_now=datetime.datetime.now())
        else:
            # If the access code is not found in the list redirect to manage all codes
            return redirect(url_for('manage_all_access_codes'))
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/extend_code/<code_to_extend>', methods=['GET', 'POST'])
def extend_access_code(code_to_extend):
    """This covers allowing the user to extend the duration of an access code.

    Allowed methods: GET, POST.

    Keyword arguments:
    code_to_extend (str) -- The id of the access code that needs extending."""
    global user, success_message

    if user.logged_in:
        code_to_manage = None

        # Find the code in the users access codes list to use
        for code in user.access_codes:
            if code.code_id == int(code_to_extend):
                code_to_manage = code
                break

        if code_to_manage is not None:
            if request.method == 'GET':
                # If the page is just loaded, render the page
                logger.log_benchmark("Extend Access Code Load")
                return render_template('manage_access_code/extend_code.html', user=user, code_to_use=code_to_manage)
            elif request.method == 'POST':
                # Check the details for extension have been provided correctly
                if len(request.form) > 0:
                    feedback = None
                    # Set feedback if code duration value is not set
                    if request.form["code_duration_number"] == "":
                        feedback = "You need to specify a duration value."
                    # Set feedback if code duration value is not numeric
                    elif not request.form["code_duration_number"].isnumeric():
                        feedback = "The duration value must be a number."
                    # Set feedback if code duration value is less than 1
                    elif int(request.form["code_duration_number"]) < 1:
                        feedback = "The duration value must be greater than 0."
                    # Set feedback if code denominator is not in the list
                    elif request.form["code_duration_type"] not in ("hours", "days"):
                        feedback = "You need to specify a duration denomination."

                    if feedback is None:
                        # If no feedback exists yet, check the expiry date that would be generated is within the
                        # acceptable date range and provide feedback if not
                        feedback = check_expiry_date_is_valid(code_to_manage.expiry,
                                                              int(request.form["code_duration_number"]),
                                                              request.form["code_duration_type"])

                    if feedback is not None:
                        # If feedback present, notify the user
                        return render_template('manage_access_code/extend_code.html', user=user,
                                               code_to_use=code_to_manage, feedback=feedback)

                    # Takes the values and regenerates the expiry
                    code_to_manage.duration_time = int(request.form["code_duration_number"])
                    code_to_manage.duration_denominator = request.form["code_duration_type"]
                    code_to_manage.generate_expiry_from_duration()

                    logger.log_benchmark("Extend Access Code - Successfully Extended")
                    success_message = "The code was successfully extended."
                    return redirect(url_for('manage_access_code', code_to_retrieve=code_to_manage.code_id))
                else:
                    # The form is empty, so notify the user they have to provide some values before submitting
                    feedback = "You must specify the values you wish to extend the code by to extend it."
                    return render_template('manage_access_code/extend_code.html', user=user, code_to_use=code_to_manage,
                                           feedback=feedback)
        else:
            # If the access code is not found in the list redirect to manage all codes
            return redirect(url_for('manage_all_access_codes'))
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/revoke_code/<code_to_revoke>', methods=['GET', 'POST'])
def revoke_access_code(code_to_revoke):
    """This covers allowing the user to revoke an access code.

    Allowed methods: GET, POST.

    Keyword arguments:
    code_to_revoke (str) -- The id of the access code that needs revoking."""
    global user, success_message

    if user.logged_in:
        code_to_manage = None

        # Find the code in the users access codes list to use
        for code in user.access_codes:
            if code.code_id == int(code_to_revoke):
                code_to_manage = code
                break

        if code_to_manage is not None:
            if request.method == 'GET':
                # If the page is just loaded, render the page
                logger.log_benchmark("Revoke Access Code Load")
                return render_template('manage_access_code/revoke_code.html', user=user, code_to_use=code_to_manage)
            elif request.method == 'POST':
                # Check the form has been populated
                if len(request.form) > 0:
                    if request.form["confirm_revoke"] == "on":
                        # Change the code expiry time to now and state to revoked, before setting success message and
                        # returning to the manage access code page
                        code_to_manage.expiry = datetime.datetime.now()
                        code_to_manage.accessed_state = AccessStates.REVOKED

                        logger.log_benchmark("Revoke Access Code - Code Revoked")
                        success_message = "The code was successfully revoked."
                        return redirect(url_for('manage_access_code', code_to_retrieve=code_to_manage.code_id))
                    else:
                        # The form is empty, so notify the user they have to provide some values before submitting
                        feedback = "You must confirm that you want to revoke the code."
                        return render_template('manage_access_code/revoke_code.html', user=user,
                                               code_to_use=code_to_manage, feedback=feedback)
                else:
                    # The form is empty, so notify the user they have to provide some values before submitting
                    feedback = "You must confirm that you want to revoke the code."
                    return render_template('manage_access_code/revoke_code.html', user=user, code_to_use=code_to_manage,
                                           feedback=feedback)
        else:
            # If the access code is not found in the list redirect to manage all codes
            return redirect(url_for('manage_all_access_codes'))
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/reactivate_code/<code_to_reactivate>', methods=['GET', 'POST'])
def reactivate_access_code(code_to_reactivate):
    """This covers allowing the user to reactivate an access code.

    Allowed methods: GET, POST.

    Keyword arguments:
    code_to_reactivate (str) -- The id of the access code that needs reactivating."""
    global user, success_message

    if user.logged_in:
        code_to_manage = None

        # Find the code in the users access codes list to use
        for code in user.access_codes:
            if code.code_id == int(code_to_reactivate):
                code_to_manage = code
                break

        if code_to_manage is not None:
            if request.method == 'GET':
                # If the page is just loaded, render the page
                logger.log_benchmark("Reactivate Access Code Load")
                return render_template('manage_access_code/reactivate_code.html', user=user, code_to_use=code_to_manage)
            elif request.method == 'POST':
                # Check the form has been populated with valid values
                feedback = None
                if len(request.form) > 0:
                    # Set feedback if code duration value is not set
                    if request.form["code_duration_number"] == "":
                        feedback = "You need to specify a duration value."
                    # Set feedback if code duration value is not numeric
                    elif not request.form["code_duration_number"].isnumeric():
                        feedback = "The duration value must be a number."
                    # Set feedback if code duration value is less than 1
                    elif int(request.form["code_duration_number"]) < 1:
                        feedback = "The duration value must be greater than 0."
                    # Set feedback if code denominator is not in the list
                    elif request.form["code_duration_type"] not in ("hours", "days"):
                        feedback = "You need to specify a duration denomination."

                    if feedback is None:
                        # If no feedback exists yet, check the expiry date that would be generated is within the
                        # acceptable date range and provide feedback if not
                        feedback = check_expiry_date_is_valid(code_to_manage.expiry,
                                                              int(request.form["code_duration_number"]),
                                                              request.form["code_duration_type"])

                    if feedback is not None:
                        return render_template('manage_access_code/reactivate_code.html', user=user,
                                               code_to_use=code_to_manage, feedback=feedback)

                    # Takes the values and regenerates the expiry, setting the state to active and setting the global
                    # success message before redirecting back to the manage access code page
                    code_to_manage.duration_time = int(request.form["code_duration_number"])
                    code_to_manage.duration_denominator = request.form["code_duration_type"]
                    code_to_manage.generate_expiry_from_duration()
                    code_to_manage.accessed_state = AccessStates.ACTIVE

                    logger.log_benchmark("Reactivate Access Code - Code Reactivated")
                    success_message = "The code was successfully reactivated."
                    return redirect(url_for('manage_access_code', code_to_retrieve=code_to_manage.code_id))
                else:
                    # The form is empty, so notify the user they have to provide some values before submitting
                    feedback = "You must specify how long the code should be reactivated for."
                    return render_template('manage_access_code/reactivate_code.html.html', user=user,
                                           code_to_use=code_to_manage, feedback=feedback)
        else:
            # If the access code is not found in the list redirect to manage all codes
            return redirect(url_for('manage_all_access_codes'))
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


@app.route('/manage_all_codes')
def manage_all_access_codes():
    """This covers the manage all codes page to allow users to see all the access codes they have generated."""
    if user.logged_in:
        logger.log_benchmark("Manage All Access Codes")
        return render_template('manage_access_code/manage_all_codes.html', user=user)
    else:
        # If the user is not logged in, direct them to the index page
        return redirect(url_for('index'))


# Errors


@app.errorhandler(404)
def page_not_found(error):
    """Handles returning the 404 template if the page isn't found."""
    return render_template('errors/404.html', user=user, err=error)


@app.errorhandler(500)
def internal_server_error(error):
    """Handles returning the 500 template if an error occurs."""
    return render_template('errors/500.html', user=user, err=error)
