import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

import unittest
import socket
import threading
from colorama import init, Fore, Style
from Database import connection
from socket.server import CafeteriaServer
init(autoreset=True)


class TestCafeteriaServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = CafeteriaServer()
        cls.server_thread = threading.Thread(target=cls.server.start)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        print(Fore.GREEN + "Server started successfully.")

    def setUp(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 9999))
        print(Fore.BLUE + "Client connected to the server.")

    def tearDown(self):
        self.client_socket.send(b"disconnect")
        self.client_socket.close()
        print(Fore.BLUE + "Client disconnected from the server.")

    def send_message(self, message):
        self.client_socket.send(message.encode("utf-8"))
        return self.client_socket.recv(1024).decode("utf-8")

    def test_add_menu_item(self):
        print(Fore.YELLOW + "Testing: Add Menu Item")
        itemName = "pasta"
        price = int(12.5)
        availabilityStatus = int(1)
        mealType = "Lunch"
        specialty = "made with herbs"
        is_deleted = int(0)
        dietary_preference = "Vegetarian"
        spice_level = "Low"
        preferred_cuisine = "North Indian"
        sweet_tooth = "Yes"
        response = self.send_message(
            f"add_menu_item|{itemName}|{price}|{availabilityStatus}|{mealType}|{specialty}|{is_deleted}|{dietary_preference}|{spice_level}|{preferred_cuisine}|{sweet_tooth}"
        )
        self.assertEqual(response, f"Food Item added in Menu : {itemName}")
        print(Fore.GREEN + "Test Passed: Add Menu Item")

    def test_get_menu(self):
        print(Fore.YELLOW + "Testing: Get Menu")
        response = self.send_message("get_menu")
        self.assertIn("Kheer", response)
        print(Fore.GREEN + "Test Passed: Get Menu")

    def test_get_menu_format(self):
        print(Fore.YELLOW + "Testing: Get Menu Format")
        response = self.send_message("get_menu")
        lines = response.split("\n")
        valid_lines = [line for line in lines if len(line.split("|")) == 11]

        for line in valid_lines:
            field_count = len(line.split("|"))
            self.assertEqual(field_count, 11)
        print(Fore.GREEN + "Test Passed: Get Menu Format")

    def test_get_menu_not_empty(self):
        print(Fore.YELLOW + "Testing: Get Menu Not Empty")
        response = self.send_message("get_menu")
        self.assertTrue(len(response) > 0)
        print(Fore.GREEN + "Test Passed: Get Menu Not Empty")

    def test_delete_menu_item(self):
        print(Fore.YELLOW + "Testing: Delete Menu Item")
        id = 1
        response = self.send_message(f"delete_menu_item|{id}")
        conn = connection.get_connection()
        cur = conn.cursor()
        sql = "select id, itemName from Menu where id = ?"
        cur.execute(sql, (id,))
        deleted_menu_item = cur.fetchone()

        if deleted_menu_item is None:
            self.assertEqual(response, "No menu item found with the given menuId.")
        else:
            id = deleted_menu_item[0]
            item_name = deleted_menu_item[1]
            self.assertEqual(
                response,
                f"Menu item deleted with menuId {id} and item name {item_name}",
            )
        print(Fore.GREEN + "Test Passed: Delete Menu Item")

    def test_get_recommendations(self):
        print(Fore.YELLOW + "Testing: Get Recommendations")
        response = self.send_message("get_recommendations")
        if response == "No recommendation for food today!":
            self.assertIn("No recommendation for food today!", response)
        else:
            self.assertTrue(response.startswith("[(") and response.endswith(")]"))
        print(Fore.GREEN + "Test Passed: Get Recommendations")


if __name__ == "__main__":
    unittest.main()
