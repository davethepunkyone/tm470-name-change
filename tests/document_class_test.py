import unittest
from classes.document_class import Document
import globals.test_globals as tg


class DocumentClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_doc = Document()
        self.test_doc.document_id = tg.test_doc_id
        self.test_doc.user_id = tg.test_user_id
        self.test_doc.complete = tg.test_state
        self.test_doc.uploaded_file_id = tg.test_uploaded_file_id
        self.test_doc.old_first_name = tg.test_old_first_name
        self.test_doc.old_surname = tg.test_old_surname
        self.test_doc.new_first_name = tg.test_first_name
        self.test_doc.new_surname = tg.test_surname
        self.test_doc.address_id = tg.test_address_id
        self.test_doc.document_verified_state = tg.test_state
        self.test_doc.document_verified_id = tg.test_doc_verified_id
     #   self.test_doc.added_datetime = tg.test_added_datetime
     #   self.test_doc.last_modified_datetime = tg.test_modified_datetime

    def test_get_doc_id(self) -> None:
        self.assertEqual(self.test_doc.document_id, tg.test_doc_id)

    def test_set_doc_id(self) -> None:
        different_id = 999
        self.test_doc.document_id = different_id
        self.assertEqual(self.test_doc.document_id, different_id)


if __name__ == '__main__':
    unittest.main()
