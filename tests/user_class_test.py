import unittest
from classes.user_class import User


class UserClassTest(unittest.TestCase):
    def test_get_first_name(self):
        test_string = "Test"
        test_user_class = User()
        test_user_class._first_name = test_string
        self.assertEqual(test_user_class.get_first_name(), test_string)

    def test_set_first_name(self):
        test_string = "Test"
        test_user_class = User()
        test_user_class.set_first_name(test_string)
        self.assertEqual(test_user_class._first_name, test_string)


if __name__ == '__main__':
    unittest.main()
