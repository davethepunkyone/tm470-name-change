import unittest
from classes.user_class import User
from classes.marriagecertificate_class import MarriageCertificate
from globals.test_globals import test_user_id, test_forenames, test_surname, test_email, test_state, test_doc1


class UserClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_user = User()
        self.test_user.user_id = test_user_id
        self.test_user.forenames = test_forenames
        self.test_user.surname = test_surname
        self.test_user.email = test_email
        self.test_user.verified_state = test_state
        self.test_user.logged_in = test_state
        self.test_user.docs = test_doc1

    def test_get_id(self) -> None:
        self.assertEqual(self.test_user.user_id, test_user_id)

    def test_set_id(self) -> None:
        different_id = 999
        self.test_user.user_id = different_id
        self.assertEqual(self.test_user.user_id, different_id)

    def test_set_invalid_id(self) -> None:
        different_id = "hello"
        with self.assertRaises(ValueError) as err:
            self.test_user.user_id = different_id
        self.assertEqual(str(err.exception), "ID provided ({0}) is not numeric or None".format(different_id))
        self.assertEqual(self.test_user.user_id, test_user_id)

    def test_get_forenames(self) -> None:
        self.assertEqual(self.test_user.forenames, test_forenames)

    def test_set_forenames(self) -> None:
        different_name = "Adam"
        self.test_user.forenames = different_name
        self.assertEqual(self.test_user.forenames, different_name)

    def test_get_surname(self) -> None:
        self.assertEqual(self.test_user.surname, test_surname)

    def test_set_surname(self) -> None:
        different_name = "Jones"
        self.test_user.surname = different_name
        self.assertEqual(self.test_user.surname, different_name)

    def test_get_email(self) -> None:
        self.assertEqual(self.test_user.email, test_email)

    def test_set_email(self) -> None:
        different_email = "test@newemail.co.uk"
        self.test_user.email = different_email
        self.assertEqual(self.test_user.email, different_email)

    def test_get_verified_state(self) -> None:
        self.assertEqual(self.test_user.verified_state, test_state)

    def test_set_verified_state(self) -> None:
        different_state = False
        self.test_user.verified_state = different_state
        self.assertEqual(self.test_user.verified_state, different_state)

    def test_set_invalid_verified_State(self) -> None:
        different_state = 2
        with self.assertRaises(ValueError) as err:
            self.test_user.verified_state = different_state
        self.assertEqual(str(err.exception),
                         "Verified State provided ({0}) is not boolean or None".format(different_state))

    def test_get_logged_in(self) -> None:
        self.assertEqual(self.test_user.logged_in, test_state)

    def test_set_logged_in(self) -> None:
        different_state = False
        self.test_user.logged_in = different_state
        self.assertEqual(self.test_user.logged_in, different_state)

    def test_get_docs(self) -> None:
        list_test_doc_1 = [test_doc1]
        self.assertEqual(self.test_user.docs, list_test_doc_1)

    def test_set_docs(self) -> None:
        self.test_user.docs.remove(test_doc1)
        different_doc = MarriageCertificate()
        different_doc2 = MarriageCertificate()
        self.test_user.docs = different_doc
        self.test_user.docs = different_doc2
        list_different_docs = [different_doc, different_doc2]
        self.assertEqual(self.test_user.docs, list_different_docs)

    def test_conversion_to_dict(self) -> None:
        self.assertEqual(self.test_user.return_user_as_dict.get("id"), test_user_id)
        self.assertEqual(self.test_user.return_user_as_dict.get("forenames"), test_forenames)
        self.assertEqual(self.test_user.return_user_as_dict.get("surname"), test_surname)
        self.assertEqual(self.test_user.return_user_as_dict.get("email"), test_email)
        self.assertEqual(self.test_user.return_user_as_dict.get("verified_state"), test_state)


if __name__ == '__main__':
    unittest.main()
