import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'module')))

import unittest
from unittest.mock import patch, MagicMock
from application import CafeteriaClient

class TestCafeteriaClient(unittest.TestCase):

    @patch('client.socket.socket')
    def setUp(self, mock_socket):
        self.mock_socket = mock_socket.return_value
        self.client = CafeteriaClient()
    
    def test_send_message(self):
        self.mock_socket.recv.return_value = b'Server response'
        response = self.client.send_message('test_message')
        self.mock_socket.send.assert_called_with(b'test_message')
        self.assertEqual(response, 'Server response')

    def test_authenticate_user(self):
        with patch('builtins.input', side_effect=['user_id', 'name', 'quit']):
            self.mock_socket.recv.return_value = b'authenticated'
            with patch('sys.exit') as mock_exit:
                self.client.authenticate_user()
                self.mock_socket.send.assert_called_with(b'authenticate|user_id|name')
                self.assertEqual(self.mock_socket.recv.call_count, 1)
                mock_exit.assert_called_once()

    def test_admin_menu(self):
        with patch('builtins.input', side_effect=[1, 'itemName', '10.0', '1', 'mealType', 'specialty', 6]):
            self.client.admin_menu()
            self.mock_socket.send.assert_any_call(b'get_menu')
            self.mock_socket.send.assert_any_call(b'discard_list')

    def test_chef_menu(self):
        with patch('builtins.input', side_effect=[1, 4]):
            self.client.chef_menu()
            self.mock_socket.send.assert_any_call(b'monthly_feedback_report')

    def test_employee_menu(self):
        with patch('builtins.input', side_effect=[1, 'user_id', '1', '5', 'comment', 8]):
            self.client.employee_menu()
            self.mock_socket.send.assert_any_call(b'add_feedback|user_id|1|5|comment')

    def test_main(self):
        with patch('builtins.input', side_effect=['user_id', 'name', 'employee']):
            self.mock_socket.recv.return_value = b'authenticated'
            with patch('client.CafeteriaClient.employee_menu') as mock_employee_menu:
                self.client.main()
                mock_employee_menu.assert_called_once()

if __name__ == '__main__':
    unittest.main()
