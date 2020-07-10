import unittest


class UserClassTest(unittest.TestCase):
    def test_two_equals_two(self):
        value_to_check = 2
        self.assertEqual(value_to_check, 2)


if __name__ == '__main__':
    unittest.main()
