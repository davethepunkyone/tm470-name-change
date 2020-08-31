import unittest
import functions.signup_functions as sf
from globals.global_variables import live_url
from classes.signup_verification_class import SignupVerification


class SignupFunctionsTest(unittest.TestCase):
    def test_confirm_email_address_value_valid_value(self):
        self.assertTrue(sf.confirm_email_address_value("test@email.com"))

    def test_confirm_email_address_value_invalid_value(self):
        self.assertFalse(sf.confirm_email_address_value("bad-email.com"))

    def test_confirm_password_value_valid_value(self):
        self.assertIsNone(sf.confirm_password_value("AbcDef123"))

    def test_confirm_password_value_invalid_length(self):
        self.assertEqual(sf.confirm_password_value("Ab1"), "The password must be at least 8 characters.")

    def test_confirm_password_value_no_caps(self):
        self.assertEqual(sf.confirm_password_value("ab1ab1ab1"), "The password requires at least one uppercase letter.")

    def test_confirm_password_value_no_lower(self):
        self.assertEqual(sf.confirm_password_value("AV1AV1AV1"), "The password requires at least one lowercase letter.")

    def test_confirm_password_value_no_number(self):
        self.assertEqual(sf.confirm_password_value("zazaZAZA"), "The password requires at least one numeric character.")

    def test_generate_code(self):
        self.assertEqual(len(sf.generate_code(3)), 3)

    def test_generate_code_longer(self):
        self.assertEqual(len(sf.generate_code(45)), 45)

    def test_generate_capcha_code(self):
        self.assertEqual(len(sf.generate_capcha_code()), 5)

    def test_generate_signup_code(self):
        self.assertEqual(len(sf.generate_signup_code()), 20)

    def test_generate_link(self):
        test_signup_record = SignupVerification(user_id=15, signup_code="ThisIsATestCode")
        self.assertEqual(sf.generate_link(test_signup_record), live_url + "/new_account_confirm/ThisIsATestCode")


if __name__ == '__main__':
    unittest.main()
