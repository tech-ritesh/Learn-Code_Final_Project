import unittest
from application import CafeteriaClient


class TestCafeteriaClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = CafeteriaClient()

    def test_authenticate_user(self):
        self.client.send_message("authenticate|1|John Doe")
        response = self.client.authenticate_user()
        self.assertIn(response, ["authenticated", "authentication_failed"])

    def test_admin_menu_add_item(self):
        response = self.client.send_message("add_menu_item|Pizza|10.0|1|Lunch|Italian")
        self.assertEqual(response, "menu_item_added")

    def test_admin_menu_view_items(self):
        response = self.client.send_message("get_menu")
        self.assertIn("Pizza", response)

    def test_employee_menu_view_recommendations(self):
        response = self.client.send_message("get_recommendations")
        self.assertIn("No recommendation for food today!", response)


if __name__ == "__main__":
    unittest.main()
