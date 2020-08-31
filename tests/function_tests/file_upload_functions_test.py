import unittest
import functions.file_upload_functions as fuf
from classes.document_class import Document


class FileUploadFunctionsTest(unittest.TestCase):
    def test_check_filetype_valid_with_valid_file(self):
        self.assertTrue(fuf.check_filetype_valid("test.png"))

    def test_check_filetype_valid_with_invalid_file(self):
        self.assertFalse(fuf.check_filetype_valid("test.doc"))

    def test_return_filetype(self):
        self.assertEqual(fuf.return_filetype("test.jpg"), ".jpg")

    def test_return_filename(self):
        item_to_check = Document(document_id=15, user_id=35)
        self.assertEqual(fuf.return_filename(item_to_check, "test.gif"), "35_15.gif")


if __name__ == '__main__':
    unittest.main()
