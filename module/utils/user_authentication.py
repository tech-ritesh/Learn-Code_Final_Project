from colorama import Fore, Style

class UserAuthentication:
    def __init__(self, client):
        self.client = client

    def authenticate_user(self, user):
        try:
            print(Fore.CYAN + "\n================== Authentication ==================\n")
            employee_id = int(input(f"Enter {user} employee ID: "))
            name = input(f"Enter {user} name: ")
            response = self.client.send_message(f"authenticate|{employee_id}|{name}")

            if response:
                print(Fore.GREEN + f"\n{user} {response}")
            else:
                print(Fore.RED + f"{user} {response}")
                exit()
        except Exception as e:
            print(Fore.RED + f"Error during authentication: {e}")
