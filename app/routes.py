import os

from flask import render_template, redirect, url_for, request
from app import app
import datetime
from werkzeug.utils import secure_filename

import globals.mock_variables as mock
import globals.global_variables as gv
import functions.general_functions as gen_functions
from classes.organisation_class import Organisation

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


@app.route('/forgotten_password')
def forgot_password():
    return render_template('forgotten_password.html', user=user)


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
    global user, incrementer_user, capcha_on_page

    if user.logged_in:
        return redirect(url_for('account_home'))
    else:
        if request.method == 'GET':
            logger.log_benchmark("Load New Account Signup")
            capcha_on_page = generate_capcha_code()
            return render_template('new_account/new_account_signup.html', user=user, capcha=capcha_on_page)
        elif request.method == 'POST':
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
                initial_feedback = check_new_user_form_values(form_data, secure_form_data)
                capcha_on_page = generate_capcha_code()  # Regenerates CAPCHA in event of any type of fail
                if initial_feedback is not None:
                    feedback = initial_feedback
                    return render_template('new_account/new_account_signup.html', user=user, capcha=capcha_on_page,
                                           feedback=feedback, form_data=form_data)
                if not request.form.__contains__("agreement"):
                    feedback = "You must agree to the terms and conditions to proceed."
                    return render_template('new_account/new_account_signup.html', user=user, capcha=capcha_on_page,
                                           feedback=feedback, form_data=form_data)
                else:
                    user = User(user_id=incrementer_user, forenames=form_data["forenames"],
                                surname=form_data["surname"], email=form_data["email"],
                                prototype_password=secure_form_data["pwd"], verified_state=False)
                    users_list.append(user)
                    incrementer_user += 1
                    signup_details = SignupVerification(signup_code=generate_signup_code(), user_id=user.user_id)
                    signup_verification_list.append(signup_details)
                    email_user_notepad_version(user, signup_details)
                    return redirect(url_for('new_account_click_link'))
            else:
                feedback = "You need to complete all the fields to create a new account."
                capcha_on_page = generate_capcha_code()
                return render_template('new_account/new_account_signup.html', user=user, capcha=capcha_on_page,
                                       feedback=feedback)


def check_new_user_form_values(form_data: dict, secure_form_data: dict):
    pw_check = confirm_password_value(secure_form_data["pwd"])

    if form_data["forenames"] == "" or form_data["surname"] == "" or form_data["email"] == "" or \
            form_data["email_confirm"] == "" or secure_form_data["pwd"] == "" or \
            secure_form_data["pwd_confirm"] == "" or secure_form_data["capcha"] == "":
        return "You need to complete all the fields to create a new account."
    elif check_user_already_exists(form_data["email"]):
        return "The email address provided is already registered on this service."
    elif form_data["email"] != form_data["email_confirm"]:
        return "The email address and confirm email address do not match."
    elif not confirm_email_address_value(form_data["email"]):
        return "The email address is not in a valid format."
    elif pw_check is not None:
        return pw_check
    elif secure_form_data["pwd"] != secure_form_data["pwd_confirm"]:
        return "The password and confirm password do not match."
    elif capcha_on_page != secure_form_data["capcha"]:
        return "The CAPCHA verification failed, please try again."
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
        logger.log_benchmark("Account Homepage")
        table_values = []
        entry_val = 1

        for doc in user.docs:
            total_codes = 0
            active_codes = 0
            expired_codes = 0
            for code in user.access_codes:
                if code.uploaded_document.document_id == doc.document_id:
                    total_codes = total_codes = + 1
                    if code.accessed_state == AccessStates.ACTIVE:
                        active_codes = active_codes = + 1
                    elif code.accessed_state == AccessStates.EXPIRED:
                        expired_codes = expired_codes = + 1

            table_row = {"doc_name": doc.document_type + " (" + doc.change_of_name_date_as_string + ")",
                         "doc_state": doc.document_verified_state,
                         "total_codes": total_codes,
                         "active_codes": active_codes,
                         "expired_codes": expired_codes}

            table_values.append(table_row)

            entry_val += 1

        return render_template('account_home.html', user=user, table_data=table_values)


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
    logger.log_benchmark("User Logout")
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
            logger.log_benchmark("Add New Document: Start")
            return render_template('add_document/add_doc_1_selection.html', user=user, divorce_on=marriage_cert_present)
        elif request.method == 'POST':
            if len(request.form) > 0:
                access_code_id_doc = request.form["doc_type"]
                if access_code_id_doc == "marriage_cert":
                    document = MarriageCertificate(document_id=incrementer_document, user_id=user.user_id,
                                                   complete=False)
                    incrementer_document += 1
                    logger.log_benchmark("Add New Document: Select Document (Marriage Certificate)")
                    return redirect(url_for('new_document_upload_image'))
                elif access_code_id_doc == "deed_poll":
                    document = DeedPoll(document_id=incrementer_document, user_id=user.user_id, complete=False)
                    incrementer_document += 1
                    logger.log_benchmark("Add New Document: Select Document (Deed Poll)")
                    return redirect(url_for('new_document_upload_image'))
                elif access_code_id_doc == "decree_absolute":
                    document = DecreeAbsolute(document_id=incrementer_document, user_id=user.user_id, complete=False)
                    incrementer_document += 1
                    logger.log_benchmark("Add New Document: Select Document (Decree Absolute)")
                    return redirect(url_for('new_document_decree_absolute_certificate'))
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


@app.route('/new_document_1a', methods=['GET', 'POST'])
def new_document_decree_absolute_certificate():
    global document

    if user.logged_in:
        if request.method == 'GET':
            return render_template('add_document/add_doc_1a_decree_absolute_selection.html', user=user,
                                   doc=document)
        elif request.method == 'POST':
            if len(request.form) > 0:
                marriage_cert_details = request.form["marriage_cert"]
                document.marriage_certificate_details = user.get_specific_listed_doc(int(marriage_cert_details))
                logger.log_benchmark("Add New Document: Decree Absolute - Select Marriage Certificate")
                return redirect(url_for('new_document_upload_image'))
            else:
                feedback = "You need to select at least one option."
                return render_template('add_document/add_doc_1a_decree_absolute_selection.html', user=user,
                                       doc=document, feedback=feedback)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_2', methods=['GET', 'POST'])
def new_document_upload_image():
    global document

    if user.logged_in:
        if request.method == 'GET':
            return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document)
        if request.method == 'POST':
            if 'user_file' not in request.files:
                # Control has not been initialized
                if document.uploaded_file_path is not None:
                    return redirect(url_for('new_document_confirm_image'))
                else:
                    feedback = "No file was uploaded."
                    return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document,
                                           feedback=feedback)
            else:
                # Control has been initialized
                file_to_use = request.files["user_file"]
                if file_to_use.filename == "" and document.uploaded_file_path is not None:
                    return redirect(url_for('new_document_confirm_image'))
                elif file_to_use.filename == "" and document.uploaded_file_path is None:
                    feedback = "No file was uploaded."
                    return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document,
                                           feedback=feedback)

                if check_filetype_valid(file_to_use.filename):
                    filename = return_filename(document, file_to_use.filename)
                    filepath = os.path.join(app.config['UPLOAD_DIRECTORY'], filename)
                    file_to_use.save(filepath)
                    document.uploaded_file_path = filename
                    logger.log_benchmark("Add New Document: Upload File")
                    return redirect(url_for('new_document_confirm_image'))
                else:
                    feedback = "The filetype provided is invalid."
                    return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=document,
                                           feedback=feedback)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_3', methods=['GET', 'POST'])
def new_document_confirm_image():
    if user.logged_in:
        if request.method == 'GET':
            return render_template('add_document/add_doc_3_confirm_image.html', user=user, doc=document)
        if request.method == 'POST':
            if len(request.form) > 0:
                if request.form["image_correct"] == "on":
                    logger.log_benchmark("Add New Document: Confirm Image Upload")
                    return redirect(url_for('new_document_add_personal_details'))
                else:
                    feedback = "You need to confirm the image has uploaded correctly."
                    return render_template('add_document/add_doc_3_confirm_image.html', user=user, doc=document,
                                           feedback=feedback)
            else:
                feedback = "You need to confirm the image has uploaded correctly."
                return render_template('add_document/add_doc_3_confirm_image.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_4', methods=['GET', 'POST'])
def new_document_add_personal_details():
    global document

    if user.logged_in:
        if request.method == 'GET':
            return render_template('add_document/add_doc_4_add_personal_details.html', user=user, doc=document)
        elif request.method == 'POST':
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
                    return render_template('add_document/add_doc_4_add_personal_details.html', user=user, doc=document,
                                           feedback=initial_feedback, form_data=form_data)
                else:
                    document.old_forenames = form_data["prev_forenames"]
                    document.old_surname = form_data["prev_surname"]
                    document.new_forenames = form_data["forenames"]
                    document.new_surname = form_data["surname"]
                    document.address = Address(house_name_no=form_data["address_house_name_no"],
                                               line_1=form_data["address_line_1"], line_2=form_data["address_line_2"],
                                               town_city=form_data["address_city"],
                                               postcode=form_data["address_postcode"])
                    logger.log_benchmark("Add New Document: Add Personal Details")
                    return redirect(url_for('new_document_confirm_personal_details'))
            else:
                feedback = "You need to complete the mandatory fields to proceed."
                return render_template('add_document/add_doc_4_add_personal_details.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        return redirect(url_for('index'))


def check_personal_details(form_data: dict) -> str or None:
    if form_data["address_house_name_no"] == "" or form_data["address_line_1"] == "" or \
            form_data["address_city"] == "" or form_data["address_postcode"] == "":
        return "The mandatory address fields have not been populated."
    elif form_data["prev_forenames"] != "" and form_data["prev_forenames"] == form_data["forenames"]:
        return "The previous forename and new forename cannot be the same."
    elif form_data["prev_surname"] != "" and form_data["prev_surname"] == form_data["surname"]:
        return "The previous surname and new surname cannot be the same."
    elif form_data["prev_forenames"] == "" and form_data["forenames"] != "":
        return "You cannot specify a new forename(s) value without providing the previous forename(s)."
    elif form_data["prev_surname"] == "" and form_data["surname"] != "":
        return "You cannot specify a new surname value without providing the previous surname."
    elif form_data["forenames"] == "" and form_data["prev_forenames"] != "":
        return "You cannot specify a previous forename(s) value without providing the new forename(s)."
    elif form_data["surname"] == "" and form_data["prev_surname"] != "":
        return "You cannot specify a previous surname value without providing the new surname."
    else:
        return None


@app.route('/new_document_5', methods=['GET', 'POST'])
def new_document_confirm_personal_details():
    if user.logged_in:
        if request.method == 'GET':
            return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user, doc=document)
        elif request.method == 'POST':
            if len(request.form) > 0:
                if request.form["personal_details_correct"] == "on":
                    logger.log_benchmark("Add New Document: Confirm Personal Details")
                    return redirect(url_for('new_document_add_document_details'))
                else:
                    feedback = "You need to confirm the details provided are correct."
                    return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user,
                                           doc=document, feedback=feedback)
            else:
                feedback = "You need to confirm the details provided are correct."
                return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_6', methods=['GET', 'POST'])
def new_document_add_document_details():
    global document

    if user.logged_in:
        if request.method == 'GET':
            return render_template('add_document/add_doc_6_add_document_details.html', user=user, doc=document)
        elif request.method == 'POST':
            if len(request.form) > 0:
                if document.document_type == "Marriage Certificate":
                    marriage_obj = {"marriage_day": request.form["marriage_date_day"],
                                    "marriage_month": request.form["marriage_date_month"],
                                    "marriage_year": request.form["marriage_date_year"],
                                    "marriage_age": request.form["marriage_age_cert"],
                                    "marriage_reg_district": request.form["marriage_reg_district"],
                                    "marriage_no": request.form["marriage_no"]}
                    initial_feedback = check_doc_details_mandatory_fields(marriage_obj)

                    if initial_feedback is not None:
                        return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                               doc=document, feedback=initial_feedback, form_data=marriage_obj)
                    else:
                        date_to_use = datetime.date(int(marriage_obj["marriage_year"]),
                                                    int(marriage_obj["marriage_month"]),
                                                    int(marriage_obj["marriage_day"]))

                        secondary_feedback = check_doc_details_dont_already_exist_for_user(date_to_use)
                        if secondary_feedback is not None:
                            return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                                   doc=document, feedback=secondary_feedback,
                                                   form_data=marriage_obj)

                        document.change_of_name_date = date_to_use
                        document.age_on_certificate = int(marriage_obj["marriage_age"])
                        document.registration_district = marriage_obj["marriage_reg_district"]
                        document.marriage_number = int(marriage_obj["marriage_no"])

                        logger.log_benchmark("Add New Document: Add Document Details")
                        return redirect(url_for('new_document_confirm_document_details'))
                elif document.document_type == "Deed Poll":
                    deed_poll_obj = {"deed_date_day": request.form["deed_date_day"],
                                     "deed_date_month": request.form["deed_date_month"],
                                     "deed_date_year": request.form["deed_date_year"]}
                    if "deed_registered" in request.form:
                        deed_poll_obj.update({"deed_registered": request.form["deed_registered"]})
                    else:
                        deed_poll_obj.update({"deed_registered": None})

                    initial_feedback = check_doc_details_mandatory_fields(deed_poll_obj)

                    if initial_feedback is not None:
                        return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                               doc=document, feedback=initial_feedback, form_data=deed_poll_obj)
                    else:
                        date_to_use = datetime.date(int(deed_poll_obj["deed_date_year"]),
                                                    int(deed_poll_obj["deed_date_month"]),
                                                    int(deed_poll_obj["deed_date_day"]))

                        secondary_feedback = check_doc_details_dont_already_exist_for_user(date_to_use)
                        if secondary_feedback is not None:
                            return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                                   doc=document, feedback=secondary_feedback,
                                                   form_data=deed_poll_obj)

                        document.change_of_name_date = date_to_use
                        document.registered_with_courts = gen_functions.yesno_to_bool(request.form["deed_registered"])

                        logger.log_benchmark("Add New Document: Add Document Details")
                        return redirect(url_for('new_document_confirm_document_details'))
                elif document.document_type == "Decree Absolute":
                    decree_absolute_obj = {"decree_date_day": request.form["decree_date_day"],
                                           "decree_date_month": request.form["decree_date_month"],
                                           "decree_date_year": request.form["decree_date_year"],
                                           "decree_issuing_court": request.form["decree_issuing_court"],
                                           "decree_no_of_matter": request.form["decree_no_of_matter"]}
                    initial_feedback = check_doc_details_mandatory_fields(decree_absolute_obj)

                    if initial_feedback is not None:
                        return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                               doc=document, feedback=initial_feedback, form_data=decree_absolute_obj)
                    else:
                        date_to_use = datetime.date(int(decree_absolute_obj["decree_date_year"]),
                                                    int(decree_absolute_obj["decree_date_month"]),
                                                    int(decree_absolute_obj["decree_date_day"]))

                        secondary_feedback = check_doc_details_dont_already_exist_for_user(date_to_use)
                        if secondary_feedback is not None:
                            return render_template('add_document/add_doc_6_add_document_details.html', user=user,
                                                   doc=document, feedback=secondary_feedback,
                                                   form_data=decree_absolute_obj)

                        document.change_of_name_date = date_to_use
                        document.issuing_court = request.form["decree_issuing_court"]
                        document.number_of_matter = request.form["decree_no_of_matter"]

                    logger.log_benchmark("Add New Document: Add Document Details")
                    return redirect(url_for('new_document_confirm_document_details'))
            else:
                feedback = "You need to complete the mandatory fields to proceed."
                return render_template('add_document/add_doc_6_add_document_details.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        return redirect(url_for('index'))


def check_doc_details_dont_already_exist_for_user(day_to_check: datetime.date) -> str or None:
    for check_users_doc in user.docs:
        if document.document_type == check_users_doc.document_type:
            if day_to_check == check_users_doc.change_of_name_date:
                return "A {} for this date ({}) already exists." \
                    .format(check_users_doc.document_type, check_users_doc.change_of_name_date_as_string)
    return None


def check_doc_details_mandatory_fields(fields_to_check: dict) -> str or None:
    if document.document_type == "Marriage Certificate":
        if fields_to_check["marriage_day"] == "" or fields_to_check["marriage_month"] == "" or \
                fields_to_check["marriage_year"] == "" or fields_to_check["marriage_age"] == "" or \
                fields_to_check["marriage_reg_district"] == "" or fields_to_check["marriage_no"] == "":
            return "All mandatory fields need to be completed to proceed."
        elif not fields_to_check["marriage_day"].isnumeric():
            return "The marriage day value must be a number."
        elif int(fields_to_check["marriage_day"]) > 31 or \
                int(fields_to_check["marriage_day"].isnumeric()) < 1:
            return "The marriage day value is not valid."
        elif not fields_to_check["marriage_month"].isnumeric():
            return "The marriage month value must be a number."
        elif int(fields_to_check["marriage_month"]) > 12 or \
                int(fields_to_check["marriage_month"]) < 1:
            return "The marriage month value is not valid."
        elif not fields_to_check["marriage_year"].isnumeric():
            return "The marriage year value must be a number."
        elif int(fields_to_check["marriage_year"]) > datetime.datetime.now().year or \
                int(fields_to_check["marriage_year"]) < 1900:
            return "The marriage year value is not valid."
        elif not fields_to_check["marriage_age"].isnumeric():
            return "The marriage age value must be a number."
        elif int(fields_to_check["marriage_age"]) > gv.maximum_age_marriage or \
                int(fields_to_check["marriage_age"]) < gv.minimum_age_marriage:
            return "The marriage age value is not valid."
        elif not fields_to_check["marriage_no"].isnumeric():
            return "The marriage number value must be a number."
        elif int(fields_to_check["marriage_no"]) < 1:
            return "The marriage number value is not valid."
        else:
            return None
    elif document.document_type == "Deed Poll":
        if fields_to_check["deed_date_day"] == "" or fields_to_check["deed_date_month"] == "" or \
                fields_to_check["deed_date_year"] == "" or fields_to_check["deed_registered"] == "":
            return "All mandatory fields need to be completed to proceed."
        elif not fields_to_check["deed_date_day"].isnumeric():
            return "The deed poll day value must be a number."
        elif int(fields_to_check["deed_date_day"]) > 31 or \
                int(fields_to_check["deed_date_day"].isnumeric()) < 1:
            return "The deed poll day value is not valid."
        elif not fields_to_check["deed_date_month"].isnumeric():
            return "The deed poll month value must be a number."
        elif int(fields_to_check["deed_date_month"]) > 12 or \
                int(fields_to_check["deed_date_month"]) < 1:
            return "The deed poll month value is not valid."
        elif not fields_to_check["deed_date_year"].isnumeric():
            return "The deed poll year value must be a number."
        elif int(fields_to_check["deed_date_year"]) > datetime.datetime.now().year or \
                int(fields_to_check["deed_date_year"]) < 1900:
            return "The deed poll year value is not valid."
        elif fields_to_check["deed_registered"] is None:
            return "You must select if the document has been registered with the courts or not."
        else:
            return None
    elif document.document_type == "Decree Absolute":
        if fields_to_check["decree_date_day"] == "" or fields_to_check["decree_date_month"] == "" or \
                fields_to_check["decree_date_year"] == "" or fields_to_check["decree_issuing_court"] == "" or \
                fields_to_check["decree_no_of_matter"] == "":
            return "All mandatory fields need to be completed to proceed."
        elif not fields_to_check["decree_date_day"].isnumeric():
            return "The decree absolute day value must be a number."
        elif int(fields_to_check["decree_date_day"]) > 31 or \
                int(fields_to_check["decree_date_day"].isnumeric()) < 1:
            return "The decree absolute day value is not valid."
        elif not fields_to_check["decree_date_month"].isnumeric():
            return "The decree absolute month value must be a number."
        elif int(fields_to_check["decree_date_month"]) > 12 or \
                int(fields_to_check["decree_date_month"]) < 1:
            return "The decree absolute month value is not valid."
        elif not fields_to_check["decree_date_year"].isnumeric():
            return "The decree absolute year value must be a number."
        elif int(fields_to_check["decree_date_year"]) > datetime.datetime.now().year or \
                int(fields_to_check["decree_date_year"]) < 1900:
            return "The decree absolute year value is not valid."
        elif not fields_to_check["decree_no_of_matter"].isnumeric():
            return "The number of matter value must be a number."
        elif int(fields_to_check["decree_no_of_matter"]) < 1:
            return "The number of matter value is not valid."
        elif document.marriage_certificate_details.change_of_name_date >= \
                datetime.date(int(fields_to_check["decree_date_year"]), int(fields_to_check["decree_date_month"]),
                              int(fields_to_check["decree_date_day"])):
            return "The Decree Absolute date cannot be before or on the associated wedding date ({})." \
                .format(document.marriage_certificate_details.change_of_name_date_as_string)
        else:
            return None
    else:
        return "The document type wasn't recognized, this error shouldn't occur."


@app.route('/new_document_7', methods=['GET', 'POST'])
def new_document_confirm_document_details():
    global document, user

    if user.logged_in:
        if request.method == 'GET':
            return render_template('add_document/add_doc_7_confirm_document_details.html', user=user, doc=document)
        elif request.method == 'POST':
            if len(request.form) > 0:
                if request.form["doc_details_correct"] == "on":
                    doc_check_feedback = check_doc_details_dont_already_exist_for_user(document.change_of_name_date)
                    # Check that the user hasn't pressed the back button after finishing and tries to add again
                    if doc_check_feedback is not None:
                        return render_template('add_document/add_doc_7_confirm_document_details.html', user=user,
                                               doc=document, feedback=doc_check_feedback)

                    document.complete = True
                    # If document isn't verified with courts, there is no way to validate it
                    if document.document_type == "Deed Poll":
                        if not document.registered_with_courts:
                            document.document_verified_state = VerifiedStates.NOT_APPLICABLE
                    user.docs.append(document)
                    logger.log_benchmark("Add New Document: Confirm Document Details")
                    return redirect(url_for('new_document_finish'))
                else:
                    feedback = "You need to confirm the details provided are correct."
                    return render_template('add_document/add_doc_7_confirm_document_details.html', user=user,
                                           doc=document, feedback=feedback)
            else:
                feedback = "You need to confirm the details provided are correct."
                return render_template('add_document/add_doc_7_confirm_document_details.html', user=user, doc=document,
                                       feedback=feedback)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_8')
def new_document_finish():
    if user.logged_in:
        logger.log_benchmark("Add New Document: Reached Finish Page")
        return render_template('add_document/add_doc_8_finish.html', user=user, doc=document, orgs=orgs)
    else:
        return redirect(url_for('index'))


@app.route('/verify_document/<code>')
def verify_document(code):
    if user.logged_in:
        if code == "0":
            logger.log_benchmark("Add New Document: Validate Document")
            return render_template('add_document/document_verification.html', user=user, doc=document)
        elif code == "1":
            document.document_verified_state = VerifiedStates.AWAITING_VERIFICATION
        elif code == "2":
            document.document_verified_state = VerifiedStates.VERIFICATION_FAILED
            document.document_verified_comment = "Document is not in good enough condition to verify."
        elif code == "9":
            document.document_verified_state = VerifiedStates.VERIFIED

        document.document_verified_org = "CYN Auto Admin"
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# New Document Processes


@app.route('/manage_all_documents')
def manage_all_documents():
    global success_message

    if user.logged_in:
        success_to_display = success_message
        if success_message is not None:
            success_message = None

        logger.log_benchmark("Manage All Documents")
        return render_template('manage_documents/manage_all_documents.html', user=user, success=success_to_display)
    else:
        return redirect(url_for('index'))


@app.route('/manage_document/<doc_id>')
def manage_document(doc_id):
    global document

    if user.logged_in:
        doc_to_manage = None
        for doc_to_check in user.docs:
            if doc_to_check.document_id == int(doc_id):
                doc_to_manage = doc_to_check
                break

        if doc_to_manage is not None:
            logger.log_benchmark("Manage Document")
            document = doc_to_manage
            return render_template('manage_documents/manage_document.html', user=user, doc=doc_to_manage)
        else:
            return redirect(url_for('manage_all_documents'))
    else:
        return redirect(url_for('index'))


@app.route('/view_document_image/<doc_id>')
def view_document_image(doc_id):
    global document

    if user.logged_in:
        doc_to_manage = None
        for doc_to_check in user.docs:
            if doc_to_check.document_id == int(doc_id):
                doc_to_manage = doc_to_check
                break

        if doc_to_manage is not None:
            logger.log_benchmark("View Document Image")
            document = doc_to_manage
            return render_template('manage_documents/view_document_image.html', user=user, doc=doc_to_manage)
        else:
            return redirect(url_for('manage_all_documents'))
    else:
        return redirect(url_for('index'))


@app.route('/remove_document/<doc_id>', methods=['GET', 'POST'])
def remove_document(doc_id):
    global user, document, success_message

    if user.logged_in:
        doc_to_manage = None
        for doc_to_check in user.docs:
            if doc_to_check.document_id == int(doc_id):
                doc_to_manage = doc_to_check
                break

        if doc_to_manage is not None:
            if request.method == 'GET':
                return render_template('manage_documents/remove_document.html', user=user, doc=doc_to_manage)
            elif request.method == 'POST':
                if len(request.form) > 0:
                    if request.form["confirm_remove"] == "on":

                        # Stop Access Codes from working
                        for codes in user.access_codes:
                            if codes.uploaded_document.document_id == doc_to_manage.document_id:
                                if codes.accessed_state in (AccessStates.ACTIVE, AccessStates.EXPIRED):
                                    codes.accessed_state = AccessStates.DOCUMENT_NO_LONGER_AVAILABLE
                                codes.expiry = datetime.datetime.now()

                        user.docs.remove(doc_to_manage)

                        success_message = "The document was successfully removed."
                        return redirect(url_for('manage_all_documents'))
                    else:
                        feedback = "You must confirm that you want to remove the document."
                        return render_template('manage_documents/remove_document.html', user=user, doc=doc_to_manage,
                                               feedback=feedback)
                else:
                    feedback = "You must confirm that you want to remove the document."
                    return render_template('manage_documents/remove_document.html', user=user, doc=doc_to_manage,
                                           feedback=feedback)
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
            logger.log_benchmark("Generate Access Code: Start")
            access_code = AccessCode()
            return render_template('generate_access_code/generate_code_1_selection.html', user=user)
        elif request.method == 'POST':
            if len(request.form) > 0:
                access_code_id_doc = request.form["user_doc"]
                access_code.uploaded_document = user.get_specific_listed_doc(int(access_code_id_doc))
                logger.log_benchmark("Generate Access Code: Document Selection")
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
                feedback = None

                form_data = {"org": request.form["org"],
                             "code_duration_number": request.form["code_duration_number"],
                             "code_duration_type": request.form["code_duration_type"]}

                if form_data["org"].isnumeric():
                    form_data.update({"org": int(request.form["org"])})

                if form_data["org"] == "":
                    feedback = "You need to select an organisation."
                elif form_data["code_duration_number"] == "":
                    feedback = "You need to specify a duration value."
                elif not form_data["code_duration_number"].isnumeric():
                    feedback = "The duration value must be a number."
                elif int(form_data["code_duration_number"]) < 1:
                    feedback = "The duration value must be greater than 0."
                elif form_data["code_duration_type"] not in ("hours", "days"):
                    feedback = "You need to specify a valid duration denomination."

                if feedback is None:
                    org_to_check = return_specific_org_from_list(orgs, int(form_data["org"]))
                    if org_to_check.requires_verified and \
                            access_code.uploaded_document.document_verified_state != VerifiedStates.VERIFIED:
                        feedback = "This organisation requires the document to be verified first."

                if feedback is None:
                    feedback = check_expiry_date_is_valid(None, int(form_data["code_duration_number"]),
                                                          form_data["code_duration_type"])

                if feedback is not None:
                    return render_template('generate_access_code/generate_code_2_details.html', user=user,
                                           code_to_use=access_code, orgs=orgs, feedback=feedback, form_data=form_data)
                else:
                    access_code.access_for_org = return_specific_org_from_list(orgs, int(form_data["org"]))
                    access_code.duration_time = int(form_data["code_duration_number"])
                    access_code.duration_denominator = form_data["code_duration_type"]
                    logger.log_benchmark("Generate Access Code: Access Code Details (Submit)")
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
            logger.log_benchmark("Generate Access Code: Confirm Details")
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

                    logger.log_benchmark("Generate Access Code: Finish")
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


@app.route('/extend_code/<code_to_extend>', methods=['GET', 'POST'])
def extend_access_code(code_to_extend):
    global user, success_message

    if user.logged_in:
        feedback = ""
        code_to_manage = None

        for code in user.access_codes:
            if code.code_id == int(code_to_extend):
                code_to_manage = code
                break

        if code_to_manage is not None:
            if request.method == 'GET':
                return render_template('manage_access_code/extend_code.html', user=user, code_to_use=code_to_manage)
            elif request.method == 'POST':
                if len(request.form) > 0:
                    feedback = None

                    if request.form["code_duration_number"] == "":
                        feedback = "You need to specify a duration value."
                    elif not request.form["code_duration_number"].isnumeric():
                        feedback = "The duration value must be a number."
                    elif int(request.form["code_duration_number"]) < 1:
                        feedback = "The duration value must be greater than 0."
                    elif request.form["code_duration_type"] not in ("hours", "days"):
                        feedback = "You need to specify a duration denomination."

                    if feedback is None:
                        feedback = check_expiry_date_is_valid(code_to_manage.expiry,
                                                              int(request.form["code_duration_number"]),
                                                              request.form["code_duration_type"])

                    if feedback is not None:
                        return render_template('manage_access_code/extend_code.html', user=user,
                                               code_to_use=code_to_manage, feedback=feedback)

                    code_to_manage.duration_time = int(request.form["code_duration_number"])
                    code_to_manage.duration_denominator = request.form["code_duration_type"]
                    code_to_manage.generate_expiry_from_duration()

                    success_message = "The code was successfully extended."
                    return redirect(url_for('manage_access_code', code_to_retrieve=code_to_manage.code_id))
                else:
                    feedback = "You must specify the values you wish to extend the code by to extend it."
                    return render_template('manage_access_code/extend_code.html', user=user, code_to_use=code_to_manage,
                                           feedback=feedback)
        else:
            return redirect(url_for('manage_all_access_codes'))
    else:
        return redirect(url_for('index'))


@app.route('/revoke_code/<code_to_revoke>', methods=['GET', 'POST'])
def revoke_access_code(code_to_revoke):
    global user, success_message

    if user.logged_in:
        feedback = ""
        code_to_manage = None

        for code in user.access_codes:
            if code.code_id == int(code_to_revoke):
                code_to_manage = code
                break

        if code_to_manage is not None:
            if request.method == 'GET':
                return render_template('manage_access_code/revoke_code.html', user=user, code_to_use=code_to_manage)
            elif request.method == 'POST':
                if len(request.form) > 0:
                    if request.form["confirm_revoke"] == "on":
                        code_to_manage.expiry = datetime.datetime.now()
                        code_to_manage.accessed_state = AccessStates.REVOKED

                        success_message = "The code was successfully revoked."
                        return redirect(url_for('manage_access_code', code_to_retrieve=code_to_manage.code_id))
                    else:
                        feedback = "You must confirm that you want to revoke the code."
                        return render_template('manage_access_code/revoke_code.html', user=user,
                                               code_to_use=code_to_manage, feedback=feedback)
                else:
                    feedback = "You must confirm that you want to revoke the code."
                    return render_template('manage_access_code/revoke_code.html', user=user, code_to_use=code_to_manage,
                                           feedback=feedback)
        else:
            return redirect(url_for('manage_all_access_codes'))
    else:
        return redirect(url_for('index'))


@app.route('/reactivate_code/<code_to_reactivate>', methods=['GET', 'POST'])
def reactivate_access_code(code_to_reactivate):
    global user, success_message

    if user.logged_in:
        feedback = ""
        code_to_manage = None

        for code in user.access_codes:
            if code.code_id == int(code_to_reactivate):
                code_to_manage = code
                break

        if code_to_manage is not None:
            if request.method == 'GET':
                return render_template('manage_access_code/reactivate_code.html', user=user, code_to_use=code_to_manage)
            elif request.method == 'POST':
                if len(request.form) > 0:
                    if request.form["code_duration_number"] == "":
                        feedback = "You need to specify a duration value."
                    elif not request.form["code_duration_number"].isnumeric():
                        feedback = "The duration value must be a number."
                    elif int(request.form["code_duration_number"]) < 1:
                        feedback = "The duration value must be greater than 0."
                    elif request.form["code_duration_type"] not in ("hours", "days"):
                        feedback = "You need to specify a duration denomination."

                    if len(feedback) > 0:
                        return render_template('manage_access_code/reactivate_code.html', user=user,
                                               code_to_use=code_to_manage, feedback=feedback)

                    code_to_manage.duration_time = int(request.form["code_duration_number"])
                    code_to_manage.duration_denominator = request.form["code_duration_type"]
                    code_to_manage.generate_expiry_from_duration()
                    code_to_manage.accessed_state = AccessStates.ACTIVE

                    success_message = "The code was successfully reactivated."
                    return redirect(url_for('manage_access_code', code_to_retrieve=code_to_manage.code_id))
                else:
                    feedback = "You must specify how long the code should be reactivated for."
                    return render_template('manage_access_code/reactivate_code.html.html', user=user,
                                           code_to_use=code_to_manage, feedback=feedback)
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
