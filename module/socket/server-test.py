import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'module')))

import unittest
import socket
import threading
from server import CafeteriaServer


class TestCafeteriaServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = CafeteriaServer()
        cls.server_thread = threading.Thread(target=cls.server.start)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    def setUp(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 9999))

    def tearDown(self):
        self.client_socket.send(b"disconnect")
        self.client_socket.close()

    def send_message(self, message):
        self.client_socket.send(message.encode("utf-8"))
        return self.client_socket.recv(1024).decode("utf-8")

    def test_authenticate(self):
        response = self.send_message("authenticate|1|John Doe")
        self.assertEqual(response, "authentication_failed")

    def test_add_menu_item(self):
        response = self.send_message("add_menu_item|Pasta|12.5|1|Lunch|Italian")
        self.assertEqual(response, "menu_item_added")

    def test_get_menu(self):
        response = self.send_message("get_menu")
        self.assertIn("Pasta", response)

    def test_delete_menu_item(self):
        response = self.send_message("delete_menu_item|1")
        self.assertEqual(response, "menu_item_deleted")

    def test_get_recommendations(self):
        response = self.send_message("get_recommendations")
        self.assertIn("No recommendation for food today!", response)


if __name__ == "__main__":
    unittest.main()
