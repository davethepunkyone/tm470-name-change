import unittest
from classes.signup_verification_class import SignupVerification
import globals.test_globals as tg


class SignupVerificationClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_signup = SignupVerification()
        self.test_signup.user_id = tg.test_signup_user
        self.test_signup.signup_code = tg.test_signup_code

    def test_get_user_id(self):
        self.assertEqual(self.test_signup.user_id, tg.test_signup_user)

    def test_set_user_id(self):
        different_id = 78457
        self.test_signup.user_id = different_id
        self.assertEqual(self.test_signup.user_id, different_id)

    def test_get_signup_code(self):
        self.assertEqual(self.test_signup.signup_code, tg.test_signup_code)

    def test_set_signup_code(self):
        different_code = "This15AnewCode70try"
        self.test_signup.signup_code = different_code
        self.assertEqual(self.test_signup.signup_code, different_code)


if __name__ == '__main__':
    unittest.main()
