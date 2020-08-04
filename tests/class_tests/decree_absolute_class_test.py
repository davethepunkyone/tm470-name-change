import unittest
import datetime
from classes.decreeabsolute_class import DecreeAbsolute
from classes.marriagecertificate_class import MarriageCertificate
import globals.test_globals as tg


class DeedPollClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_decree = DecreeAbsolute()
        self.test_decree.marriage_certificate_details = MarriageCertificate()
        self.test_decree.marriage_certificate_details.marriage_number = tg.test_marriage_no
        self.test_decree.decree_absolute_date = tg.test_decree_absolute_date
        self.test_decree.issuing_court = tg.test_issuing_court
        self.test_decree.number_of_matter = tg.test_no_of_matter

    def test_get_marriage_certificate_details(self) -> None:
        self.assertEqual(self.test_decree.marriage_certificate_details.marriage_number, tg.test_marriage_no)

    def test_set_marriage_certificate_details(self) -> None:
        different_certificate = MarriageCertificate()
        different_certificate.marriage_number = 99
        self.test_decree.marriage_certificate_details = different_certificate
        self.assertEqual(self.test_decree.marriage_certificate_details, different_certificate)

    def test_get_decree_absolute_date(self) -> None:
        self.assertEqual(self.test_decree.decree_absolute_date, tg.test_decree_absolute_date)

    def test_set_decree_absolute_date(self) -> None:
        different_date = datetime.date(2018, 11, 17)
        self.test_decree.decree_absolute_date = different_date
        self.assertEqual(self.test_decree.decree_absolute_date, different_date)

    def test_get_issuing_court(self) -> None:
        self.assertEqual(self.test_decree.issuing_court, tg.test_issuing_court)

    def test_set_issuing_court(self) -> None:
        different_court = "Newcastle Crown Court"
        self.test_decree.issuing_court = different_court
        self.assertEqual(self.test_decree.issuing_court, different_court)

    def test_get_number_of_matter(self) -> None:
        self.assertEqual(self.test_decree.issuing_court, tg.test_issuing_court)

    def test_set_number_of_matter(self) -> None:
        different_matter = "Z9548"
        self.test_decree.issuing_court = different_matter
        self.assertEqual(self.test_decree.issuing_court, different_matter)


if __name__ == '__main__':
    unittest.main()
