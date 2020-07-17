import unittest
import datetime
from classes.deedpoll_class import DeedPoll
import globals.test_globals as tg


class DeedPollClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_deed = DeedPoll()
        self.test_deed.name_change_date = tg.test_change_name_date
        self.test_deed.registered_with_courts = tg.test_changed_with_courts

    def test_get_name_change_date(self) -> None:
        self.assertEqual(self.test_deed.name_change_date, tg.test_change_name_date)

    def test_set_doc_id(self) -> None:
        different_date = datetime.date(2020, 2, 2)
        self.test_deed.name_change_date = different_date
        self.assertEqual(self.test_deed.name_change_date, different_date)

    def test_get_registered_with_courts(self) -> None:
        self.assertEqual(self.test_deed.registered_with_courts, tg.test_changed_with_courts)

    def test_set_registered_with_courts(self) -> None:
        different_reg_state = False
        self.test_deed.registered_with_courts = different_reg_state
        self.assertEqual(self.test_deed.registered_with_courts, different_reg_state)


if __name__ == '__main__':
    unittest.main()
