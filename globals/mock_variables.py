from classes.organisation_class import Organisation
from classes.user_class import User
from classes.marriagecertificate_class import MarriageCertificate
from classes.deedpoll_class import DeedPoll
from classes.accesscode_class import AccessCode
from classes.enums import VerifiedStates, AccessStates
import datetime


def mock_list_of_organisations() -> list:
    mock_org_1 = Organisation(org_id=50, org_name="Testing Organisation 1", requires_verified=True,
                              avg_time_to_process_days=3)
    mock_org_2 = Organisation(org_id=55, org_name="Another Testing Organisation", requires_verified=False,
                              avg_time_to_process_days=14)
    mock_org_3 = Organisation(org_id=57, org_name="Open University", requires_verified=False,
                              avg_time_to_process_days=5)

    return [mock_org_1, mock_org_2, mock_org_3]


def mock_list_of_users() -> list:
    # Can be used by all
    org1 = mock_list_of_organisations().__getitem__(0)

    # User 1
    doc1 = MarriageCertificate(document_id=100, change_of_name_date=datetime.date(2020, 2, 1),
                               document_verified_state=VerifiedStates.VERIFIED)

    mock_user_1 = User(user_id=5, forenames="Testy", surname="McTesterson", email= "testemail1@testing.com",
                       prototype_password="test1", verified_state=True, docs=doc1)

    # User 2
    doc2 = MarriageCertificate(document_id=200, change_of_name_date=datetime.date(2019, 7, 4),
                               document_verified_state=VerifiedStates.VERIFIED)

    doc3 = DeedPoll(document_id=201, change_of_name_date=datetime.date(2018, 12, 25),
                    document_verified_state=VerifiedStates.AWAITING_VERIFICATION)

    code1 = AccessCode(code_id=1474, generated_code="987654", expiry=datetime.datetime(2020, 9, 1, 12, 35, 12),
                       uploaded_document=doc2, access_for_org=org1, accessed_state=AccessStates.EXPIRED)

    mock_user_2 = User(user_id=16, forenames="Miguel Marcel", surname="Tablot", email="mmt@testing.com",
                       prototype_password="test2", verified_state=True, docs=[doc2, doc3], access_codes=code1)

    # User 3
    mock_user_3 = User(user_id=24, forenames="Jonathan", surname="Doe", email="jdoe@testing.co.uk",
                       prototype_password="test3", verified_state=True)

    return [mock_user_1, mock_user_2, mock_user_3]
