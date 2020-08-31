import unittest
from classes.address_class import Address
import globals.test_globals as tg


class SignupVerificationClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_address = Address()
        self.test_address.house_name_no = tg.test_alt_address_house_name
        self.test_address.line_1 = tg.test_alt_address_line_1
        self.test_address.line_2 = tg.test_alt_address_line_2
        self.test_address.town_city = tg.test_alt_address_town
        self.test_address.postcode = tg.test_alt_address_postcode

    def test_get_house_name_no(self):
        self.assertEqual(self.test_address.house_name_no, tg.test_alt_address_house_name)

    def test_set_house_name_no(self):
        different_house = "15"
        self.test_address.house_name_no = different_house
        self.assertEqual(self.test_address.house_name_no, different_house)

    def test_get_line_1(self):
        self.assertEqual(self.test_address.line_1, tg.test_alt_address_line_1)

    def test_set_line_1(self):
        different_line = "Testington Estate"
        self.test_address.line_1 = different_line
        self.assertEqual(self.test_address.line_1, different_line)

    def test_get_line_2(self):
        self.assertEqual(self.test_address.line_2, tg.test_alt_address_line_2)

    def test_set_line_2(self):
        different_line = "Testington Road"
        self.test_address.line_2 = different_line
        self.assertEqual(self.test_address.line_2, different_line)

    def test_get_town_city(self):
        self.assertEqual(self.test_address.town_city, tg.test_alt_address_town)

    def test_set_town_city(self):
        different_town = "Testington"
        self.test_address.town_city = different_town
        self.assertEqual(self.test_address.town_city, different_town)

    def test_get_postcode(self):
        self.assertEqual(self.test_address.postcode, tg.test_alt_address_postcode)

    def test_set_postcode(self):
        different_postcode = "TE57 1NG"
        self.test_address.postcode = different_postcode
        self.assertEqual(self.test_address.postcode, different_postcode)


if __name__ == '__main__':
    unittest.main()
