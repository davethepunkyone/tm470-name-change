import unittest
import functions.org_functions as of
from classes.organisation_class import Organisation


class OrgFunctionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_org_1 = Organisation(org_id=99, org_name="Unit Test Org 1", requires_verified=True,
                                       avg_time_to_process_days=58)
        self.test_org_2 = Organisation(org_id=158, org_name="Unit Test Org 2", requires_verified=False,
                                       avg_time_to_process_days=7)

        self.org_list = [self.test_org_1, self.test_org_2]

    def test_return_specific_org_from_list_valid_org(self):
        self.assertEqual(of.return_specific_org_from_list(self.org_list, 158), self.test_org_2)

    def test_return_specific_org_from_list_invalid_org(self) -> None:
        with self.assertRaises(ValueError) as err:
            of.return_specific_org_from_list(self.org_list, 1)
        self.assertEqual(str(err.exception), "Org ID provided (1) is not in the list of organisations")


if __name__ == '__main__':
    unittest.main()
