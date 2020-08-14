from flask import render_template, redirect, url_for, request
from app import app
import datetime
import globals.mock_variables as mock

from classes.user_class import User
from classes.marriagecertificate_class import MarriageCertificate
from classes.deedpoll_class import DeedPoll
from classes.accesscode_class import AccessCode
from classes.enums import VerifiedStates, AccessStates
from functions.org_functions import return_specific_org_from_list

user = User()
orgs = mock.mock_list_of_organisations()

doc = {"type": "Marriage Certificate"}
# Marriage Certificate | Deed Poll | Decree Absolute
access_code = AccessCode()


@app.route('/')
@app.route('/index')
def index():
    if user.logged_in:
        return redirect(url_for('account_home'))
    else:
        return render_template('index.html', user=user)


@app.route('/test/<test_conditions>')
def test(test_conditions):
    global user
    user = User()
    if test_conditions == "1":
        user.email = "testemail1@testing.com"
        user.logged_in = True
        doc1 = MarriageCertificate()
        doc1.document_id = 100
        doc1.change_of_name_date = datetime.date(2020, 2, 1)
        doc1.document_verified_state = VerifiedStates.VERIFIED
        user.docs = doc1
    elif test_conditions == "2":
        user.email = "testemail2@testing.com"
        user.logged_in = True
        doc2 = DeedPoll()
        doc2.document_id = 200
        doc2.change_of_name_date = datetime.date(2019, 7, 4)
        doc2.document_verified_state = VerifiedStates.VERIFIED
        doc3 = MarriageCertificate()
        doc3.document_id = 201
        doc3.change_of_name_date = datetime.date(2018, 12, 25)
        doc3.document_verified_state = VerifiedStates.AWAITING_VERIFICATION
        org1 = orgs.__getitem__(0)
        code1 = AccessCode()
        code1.code_id = 1474
        code1.generated_code = "987654"
        code1.expiry = datetime.datetime(2020, 9, 1, 12, 35, 12)
        code1.uploaded_document = doc2
        code1.access_for_org = org1
        code1.accessed_state = AccessStates.EXPIRED
        user.docs = doc2
        user.docs = doc3
        user.access_codes = code1
    elif test_conditions == "3":
        user.email = "test3@testing.com"
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


@app.route('/new_account_signup')
def new_account_signup():
    if user.logged_in:
        return redirect(url_for('account_home'))
    else:
        return render_template('new_account/new_account_signup.html', user=user)


@app.route('/new_account_click_link')
def new_account_click_link():
    if user.logged_in:
        return redirect(url_for('account_home'))
    else:
        return render_template('new_account/new_account_signup_clicklink.html', user=user)


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


@app.route('/new_document_1')
def new_document_selection():
    if user.logged_in:
        return render_template('add_document/add_doc_1_selection.html', user=user)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_2')
def new_document_upload_image():
    if user.logged_in:
        return render_template('add_document/add_doc_2_upload_image.html', user=user, doc=doc)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_3')
def new_document_confirm_image():
    if user.logged_in:
        return render_template('add_document/add_doc_3_confirm_image.html', user=user, doc=doc)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_4')
def new_document_add_personal_details():
    if user.logged_in:
        return render_template('add_document/add_doc_4_add_personal_details.html', user=user, doc=doc)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_5')
def new_document_confirm_personal_details():
    if user.logged_in:
        return render_template('add_document/add_doc_5_confirm_personal_details.html', user=user, doc=doc)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_6')
def new_document_add_document_details():
    if user.logged_in:
        return render_template('add_document/add_doc_6_add_document_details.html', user=user, doc=doc)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_7')
def new_document_confirm_document_details():
    if user.logged_in:
        return render_template('add_document/add_doc_7_confirm_document_details.html', user=user, doc=doc)
    else:
        return redirect(url_for('index'))


@app.route('/new_document_8')
def new_document_finish():
    if user.logged_in:
        return render_template('add_document/add_doc_8_finish.html', user=user, doc=doc)
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
        document_found = False
        for document in user.docs:
            if document.document_id == int(doc_id):
                doc_to_manage = document
                document_found = True
                break

        if document_found:
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
    if user.logged_in:
        feedback = ""
        if request.method == 'GET':
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


@app.route('/generate_access_code_3')
def generate_code_confirm_access_details():
    if user.logged_in:
        return render_template('generate_access_code/generate_code_3_confirm_details.html', user=user,
                               code_to_use=access_code)
    else:
        return redirect(url_for('index'))


# Manage Access Codes Processes


@app.route('/manage_code/<code_to_retrieve>')
def manage_access_code(code_to_retrieve):
    if user.logged_in:
        code_found = False
        for code in user.access_codes:
            if code.code_id == int(code_to_retrieve):
                code_to_manage = code
                code_found = True
                break

        if code_found:
            return render_template('manage_access_code/manage_code.html', user=user, code_to_use=code_to_manage)
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
