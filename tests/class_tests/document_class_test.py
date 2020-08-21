import unittest
import datetime
from classes.document_class import Document
from classes.enums import VerifiedStates
import globals.test_globals as tg


class DocumentClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_doc = Document()
        self.test_doc.document_id = tg.test_doc_id
        self.test_doc.document_type = tg.test_doc_type
        self.test_doc.user_id = tg.test_user_id
        self.test_doc.complete = tg.test_state
        self.test_doc.uploaded_file_path = tg.test_uploaded_file_path
        self.test_doc.old_forenames = tg.test_old_forenames
        self.test_doc.old_surname = tg.test_old_surname
        self.test_doc.new_forenames = tg.test_forenames
        self.test_doc.new_surname = tg.test_surname
        self.test_doc.address_id = tg.test_address_id
        self.test_doc.document_verified_state = tg.test_doc_state
        self.test_doc.document_verified_id = tg.test_doc_verified_id
        self.test_doc.change_of_name_date = tg.test_doc_added_datetime
        self.test_doc.added_datetime = tg.test_added_datetime
        self.test_doc.last_modified_datetime = tg.test_modified_datetime

    def test_get_doc_id(self) -> None:
        self.assertEqual(self.test_doc.document_id, tg.test_doc_id)

    def test_set_doc_id(self) -> None:
        different_id = 999
        self.test_doc.document_id = different_id
        self.assertEqual(self.test_doc.document_id, different_id)

    def test_get_doc_type(self) -> None:
        self.assertEqual(self.test_doc.document_id, tg.test_doc_id)

    def test_set_doc_type(self) -> None:
        different_type = "Decree Absolute"
        self.test_doc.document_type = different_type
        self.assertEqual(self.test_doc.document_type, different_type)

    def test_get_user_id(self) -> None:
        self.assertEqual(self.test_doc.user_id, tg.test_user_id)

    def test_set_user_id(self) -> None:
        different_id = 9999
        self.test_doc.user_id = different_id
        self.assertEqual(self.test_doc.user_id, different_id)

    def test_get_complete(self) -> None:
        self.assertEqual(self.test_doc.complete, tg.test_state)

    def test_set_complete(self) -> None:
        different_state = False
        self.test_doc.complete = different_state
        self.assertEqual(self.test_doc.complete, different_state)

    def test_get_uploaded_file_path(self) -> None:
        self.assertEqual(self.test_doc.uploaded_file_path, tg.test_uploaded_file_path)

    def test_set_uploaded_file_path(self) -> None:
        different_path = "/uploads/11111_99999.png"
        self.test_doc.uploaded_file_path = different_path
        self.assertEqual(self.test_doc.uploaded_file_path, different_path)

    def test_get_old_first_name(self) -> None:
        self.assertEqual(self.test_doc.old_forenames, tg.test_old_forenames)

    def test_set_old_first_name(self) -> None:
        different_name = "Alan"
        self.test_doc.old_first_name = different_name
        self.assertEqual(self.test_doc.old_first_name, different_name)

    def test_get_old_surname(self) -> None:
        self.assertEqual(self.test_doc.old_surname, tg.test_old_surname)

    def test_set_old_surname(self) -> None:
        different_name = "Appleby"
        self.test_doc.old_surname = different_name
        self.assertEqual(self.test_doc.old_surname, different_name)

    def test_get_new_first_name(self) -> None:
        self.assertEqual(self.test_doc.new_forenames, tg.test_forenames)

    def test_set_new_first_name(self) -> None:
        different_name = "Zack"
        self.test_doc.new_forenames = different_name
        self.assertEqual(self.test_doc.new_forenames, different_name)

    def test_get_new_surname(self) -> None:
        self.assertEqual(self.test_doc.new_surname, tg.test_surname)

    def test_set_new_surname(self) -> None:
        different_name = "Zackerson"
        self.test_doc.new_surname = different_name
        self.assertEqual(self.test_doc.new_surname, different_name)

    def test_get_address_id(self) -> None:
        self.assertEqual(self.test_doc.address_id, tg.test_address_id)

    def test_set_address_id(self) -> None:
        different_id = 111111
        self.test_doc.address_id = different_id
        self.assertEqual(self.test_doc.address_id, different_id)

    def test_get_change_of_name_date(self) -> None:
        self.assertEqual(self.test_doc.change_of_name_date, tg.test_doc_added_datetime)

    def test_set_change_of_name_date(self) -> None:
        different_date = datetime.date(2019, 10, 3)
        self.test_doc.change_of_name_date = different_date
        self.assertEqual(self.test_doc.change_of_name_date, different_date)

    def test_get_document_verified_state(self) -> None:
        self.assertEqual(self.test_doc.document_verified_state, tg.test_doc_state)

    def test_set_document_verified_state(self) -> None:
        different_state = VerifiedStates.AWAITING_VERIFICATION
        self.test_doc.document_verified_state = different_state
        self.assertEqual(self.test_doc.document_verified_state, different_state)

    def test_get_document_verified_id(self) -> None:
        self.assertEqual(self.test_doc.document_verified_id, tg.test_doc_verified_id)

    def test_set_document_verified_id(self) -> None:
        different_id = 111111
        self.test_doc.document_verified_id = different_id
        self.assertEqual(self.test_doc.document_verified_id, different_id)

    def test_get_added_datetime(self) -> None:
        self.assertEqual(self.test_doc.added_datetime, tg.test_added_datetime)

    def test_set_added_datetime(self) -> None:
        different_datetime = datetime.datetime(2020, 2, 1, 11, 12, 13)
        self.test_doc.added_datetime = different_datetime
        self.assertEqual(self.test_doc.added_datetime, different_datetime)

    def test_get_last_modified_datetime(self) -> None:
        self.assertEqual(self.test_doc.last_modified_datetime, tg.test_modified_datetime)

    def test_set_last_modified_datetime(self) -> None:
        different_datetime = datetime.datetime(2020, 12, 11, 23, 49, 44)
        self.test_doc.last_modified_datetime = different_datetime
        self.assertEqual(self.test_doc.last_modified_datetime, different_datetime)


if __name__ == '__main__':
    unittest.main()
