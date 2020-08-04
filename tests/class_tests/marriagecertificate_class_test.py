import unittest
import datetime
from classes.marriagecertificate_class import MarriageCertificate
import globals.test_globals as tg
import globals.global_variables as gv


class MarriageCertClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cert = MarriageCertificate()
        self.test_cert.marriage_date = tg.test_marriage_date
        self.test_cert.age_on_certificate = tg.test_age_on_cert
        self.test_cert.certificate_number = tg.test_cert_number
        self.test_cert.registration_district = tg.test_registration_district
        self.test_cert.marriage_number = tg.test_marriage_no

    def test_get_doc_id(self) -> None:
        self.assertEqual(self.test_cert.marriage_date, tg.test_marriage_date)

    def test_set_doc_id(self) -> None:
        different_date = datetime.date(2020, 1, 1)
        self.test_cert.marriage_date = different_date
        self.assertEqual(self.test_cert.marriage_date, different_date)

    def test_get_age_on_certificate(self) -> None:
        self.assertEqual(self.test_cert.age_on_certificate, tg.test_age_on_cert)

    def test_set_age_on_certificate(self) -> None:
        different_age = 20
        self.test_cert.age_on_certificate = different_age
        self.assertEqual(self.test_cert.age_on_certificate, different_age)

    def test_set_age_too_young(self) -> None:
        different_age = gv.minimum_age_marriage - 2
        with self.assertRaises(AttributeError) as err:
            self.test_cert.age_on_certificate = different_age
        self.assertEqual(str(err.exception), "The age provided ({0}) is too young (minimum = {1}).".format(
            different_age, gv.minimum_age_marriage))
        self.assertEqual(self.test_cert.age_on_certificate, tg.test_age_on_cert)

    def test_set_age_too_old(self) -> None:
        different_age = gv.maximum_age_marriage + 2
        with self.assertRaises(AttributeError) as err:
            self.test_cert.age_on_certificate = different_age
        self.assertEqual(str(err.exception), "The age provided ({0}) is too old (maximum = {1}).".format(
            different_age, gv.maximum_age_marriage))
        self.assertEqual(self.test_cert.age_on_certificate, tg.test_age_on_cert)

    def test_get_certificate_number(self) -> None:
        self.assertEqual(self.test_cert.certificate_number, tg.test_cert_number)

    def test_set_certificate_number(self) -> None:
        different_cert = "Z4978B"
        self.test_cert.certificate_number = different_cert
        self.assertEqual(self.test_cert.certificate_number, different_cert)

    def test_get_registration_district(self) -> None:
        self.assertEqual(self.test_cert.registration_district, tg.test_registration_district)

    def test_set_registration_district(self) -> None:
        different_district = "City of London"
        self.test_cert.registration_district = different_district
        self.assertEqual(self.test_cert.registration_district, different_district)

    def test_get_marriage_number(self) -> None:
        self.assertEqual(self.test_cert.marriage_number, tg.test_marriage_no)

    def test_set_marriage_number(self) -> None:
        different_number = 125
        self.test_cert.marriage_number = different_number
        self.assertEqual(self.test_cert.marriage_number, different_number)

    def test_set_marriage_number_too_low(self) -> None:
        different_number = -1
        with self.assertRaises(AttributeError) as err:
            self.test_cert.marriage_number = different_number
        self.assertEqual(str(err.exception), "The marriage number provided ({0}) is too low (minimum = 1).".format(
            different_number))
        self.assertEqual(self.test_cert.marriage_number, tg.test_marriage_no)


if __name__ == '__main__':
    unittest.main()
