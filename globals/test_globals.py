"""This file contains all the variables used for unit testing different elements of the system to ensure
a stable build."""

import datetime
from classes.marriagecertificate_class import MarriageCertificate
from classes.address_class import Address
import classes.enums as enums


# User Class Test
test_user_id = 100
test_forenames = "Testy"
test_surname = "McTesterson"
test_email = "testymctesterson@test.com"
test_state = True

# Test Address
test_address = Address(house_name_no=742, line_1="Address Line 1", line_2="Address Line 2", town_city="Testtown",
                       postcode="AB12 3CD")

test_alt_address_house_name = "Burlington Manor"
test_alt_address_line_1 = "Burlington Estate"
test_alt_address_line_2 = "Burlington Road"
test_alt_address_town = "Burlington"
test_alt_address_postcode = "BU7 7ON"

# Document Class Test
test_doc_id = 300
test_doc_type = "Marriage Certificate"
test_uploaded_file_path = "/uploads/1_300.jpg"
test_old_forenames = "Miguel"
test_old_surname = "El Testo"
test_doc_state = enums.VerifiedStates.VERIFIED
test_doc_verified_id = 17221
test_doc_added_datetime = datetime.date(2018, 4, 15)
test_added_datetime = datetime.datetime(2020, 6, 2, 12, 17, 44)
test_modified_datetime = datetime.datetime(2020, 8, 1, 7, 59, 59)

# Marriage Certificate Class Test
test_marriage_date = datetime.date(2019, 7, 4)
test_age_on_cert = 25
test_cert_number = "A741"
test_registration_district = "Exeter"
test_marriage_no = 41

# Deed Poll Class Test
test_deed_poll_date = datetime.date(2015, 7, 4)
test_changed_with_courts = True

# Decree Absolute Class Test
test_decree_absolute_date = datetime.date(2020, 4, 25)
test_issuing_court = "Plymouth"
test_no_of_matter = "A41"

# Test Doc
test_doc1 = MarriageCertificate()
test_doc1.document_id = 400

# Test Signup Verification
test_signup_user = 66
test_signup_code = "TESTcode123ABC"
