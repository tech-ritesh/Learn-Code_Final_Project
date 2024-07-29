# module/interfaces/user_interface.py
from abc import ABC, abstractmethod

class UserInterface(ABC):
    
    @abstractmethod
    def main_menu(self):
        pass
    
    @abstractmethod
    def authenticate_user(self):
        pass
