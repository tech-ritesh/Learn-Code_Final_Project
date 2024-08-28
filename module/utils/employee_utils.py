from colorama import Fore, Style
from tabulate import tabulate
import ast
import re
from logistics.notifications import Notification
from Authentication.login import Login

class NotificationsHandler:
    def __init__(self, client):
        self.client = client

    def display_notifications(self):
        try:
            notifications = Notification.get_notification()
            if notifications:
                print(Fore.YELLOW + "\nNotifications!! :\n")
                for item in notifications:
                    print(Fore.YELLOW + f"{item[0]} on date: {item[1].strftime('%Y-%m-%d')} time: {item[1].strftime('%H:%M:%S')}")
            else:
                print(Fore.CYAN + "No new notifications for today!!")
        except Exception as e:
            print(Fore.RED + f"Error displaying notifications: {e}")

class UserInteraction:
    @staticmethod
    def get_main_menu_choice():
        print(Fore.LIGHTRED_EX + "================== Chef Section ==================")
        print(Fore.YELLOW + "\n1. View Feedback Report\n2. Roll Out Menu Items\n3. View Menu\n4. Add Menu Item\n5. Update Menu Item\n6. Delete Menu Item\n7. View Employee Votes\n8. Final Recommendation\n9. Exit")
        return int(input("Enter your choice: "))

    @staticmethod
    def invalid_choice():
        print(Fore.RED + "Invalid choice. Please try again.")


    @staticmethod
    def exit_program():
        print(Fore.GREEN + "Thanks for visiting Cafeteria! Good Bye!!")
        exit()

class FeedbackProcessor:
    def __init__(self, client_communication):
        self.client_communication = client_communication

    def give_feedback(self):
        try:
            user_id = UserInputHandler.get_user_id()
            menu_id = UserInputHandler.get_menu_id()

            validation_response = self.client_communication.send_message(
                f"validate_feedback|{menu_id}|{user_id}"
            )

            if "No" in validation_response:
                print(Fore.RED + "❌ " + validation_response + Style.RESET_ALL)
            else:
                rating = UserInputHandler.get_rating()
                comment = UserInputHandler.get_comment()
                result = self.client_communication.send_message(
                    f"add_feedback|{user_id}|{menu_id}|{rating}|{comment}"
                )
                print(Fore.GREEN + "✅ " + result + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"❌ Error giving feedback: {e}" + Style.RESET_ALL)


class UserInputHandler:
    @staticmethod
    def get_user_id():
        return int(input("Enter your User ID: "))

    @staticmethod
    def get_menu_id():
        return int(input("Enter menu ID: "))

    @staticmethod
    def get_rating():
        return input("Enter the rating (1-5): ")

    @staticmethod
    def get_comment():
        return input("Enter the comment (e.g., nice taste, delicious, etc.): ")


class DataRetriever:
    def __init__(self, client, user_login):
        self.client = client
        self.user_login = user_login

    def get_feedback(self):
        try:
            feedback_str = self.client.send_message("get_feedback")
            return feedback_str
        except Exception as e:
            raise Exception(f"Error retrieving feedback data: {e}")

    def get_recommendations(self):
        try:
            response = self.client.send_message("employee_view_recommendation")
            return response
        except Exception as e:
            raise Exception(f"Error retrieving recommendations: {e}")

    def get_employee_id(self):
        return int(input("Enter employee id: "))

    def get_name(self):
        return input("Enter your name: ")

    def authenticate_user(self, employee_id, name):
        return self.user_login.authenticate(employee_id, name)

    def get_preferences(self):
        dietary_preference = input(
            "Please select one (Vegetarian/Non-Vegetarian/Eggetarian): "
        )
        spice_level = input("Please select your spice level (High/Medium/Low): ")
        preferred_cuisine = input(
            "What do you prefer most (North Indian/South Indian/Other): "
        )
        sweet_tooth = input("Do you have a sweet tooth? (Yes/No): ")
        return dietary_preference, spice_level, preferred_cuisine, sweet_tooth

    def get_user_preference(self, employee_id):
        response = self.client.send_message(f"user_preference|{employee_id}")
        return response


class DataParser:
    @staticmethod
    def parse_feedback(feedback_str):
        try:
            feedback = ast.literal_eval(feedback_str)
            return feedback
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Error parsing feedback data: {e}")

    @staticmethod
    def format_feedback(feedback):
        return [
            (
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                item[5],
            )
            for item in feedback
        ]

    @staticmethod
    def parse_recommendations(response):
        try:
            recommendations = ast.literal_eval(response)
            return recommendations
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Error processing recommendations data: {e}")

    @staticmethod
    def format_recommendations(recommendations):
        return {
            meal_type: [
                (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                )
                for item in items
            ]
            for meal_type, items in recommendations.items()
        }


class DataDisplay:
    @staticmethod
    def display_feedback(feedback_formatted):
        columns = ["id", "userId", "menuId", "itemName", "Rating", "Comment"]
        print(
            f"{Fore.CYAN}{tabulate(feedback_formatted, headers=columns, tablefmt='grid')}{Style.RESET_ALL}"
        )

    @staticmethod
    def display_recommendations(recommendations_formatted):
        columns = [
            "menuId",
            "itemName",
            "mealType",
            "recommendationDate",
            "averageRating",
        ]

        for meal_type, rows in recommendations_formatted.items():
            print(Fore.LIGHTMAGENTA_EX + f"\n{meal_type} Recommendations:\n")
            if rows:
                print(
                    f"{Fore.CYAN}{tabulate(rows, headers=columns, tablefmt='grid')}{Style.RESET_ALL}"
                )
            else:
                print(Fore.CYAN + "No recommendations available.")

    @staticmethod
    def print_message(message, color):
        print(f"{color}{message}{Fore.RESET}")

    @staticmethod
    def print_success(message):
        DataDisplay.print_message(message, Fore.GREEN)

    @staticmethod
    def print_error(message):
        DataDisplay.print_message(message, Fore.RED)

    @staticmethod
    def print_info(message):
        DataDisplay.print_message(message, Fore.CYAN)

    @staticmethod
    def print_table(data, columns):
        print(
            f"{Fore.CYAN}{tabulate(data, headers=columns, tablefmt='grid')}{Style.RESET_ALL}"
        )

    @staticmethod
    def print_no_data(message):
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

    @staticmethod
    def print_warning(message):
        DataDisplay.print_message(message, Fore.YELLOW)


class DataUpdater:
    def __init__(self, client):
        self.client = client

    def update_profile(
        self,
        employee_id,
        dietary_preference,
        spice_level,
        preferred_cuisine,
        sweet_tooth,
    ):
        response = self.client.send_message(
            f"update_profile|{employee_id}|{dietary_preference}|{spice_level}|{preferred_cuisine}|{sweet_tooth}"
        )
        return response


class ProfileProcessor:
    def __init__(self, client, user_login):
        self.data_retriever = DataRetriever(client, user_login)
        self.data_updater = DataUpdater(client)

    def update_profile(self):
        try:
            DataDisplay.print_info("Please suggest the below preferences of yours: \n")
            employee_id = self.data_retriever.get_employee_id()
            name = self.data_retriever.get_name()

            if self.data_retriever.authenticate_user(employee_id, name):
                DataDisplay.print_success("Authenticated")
            else:
                DataDisplay.print_error("Authentication failed")
                return

            dietary_preference, spice_level, preferred_cuisine, sweet_tooth = (
                self.data_retriever.get_preferences()
            )
            response = self.data_updater.update_profile(
                employee_id,
                dietary_preference,
                spice_level,
                preferred_cuisine,
                sweet_tooth,
            )
            DataDisplay.print_success(response)
        except Exception as e:
            DataDisplay.print_error(f"Error updating profile: {e}")


class DataProcessor:
    @staticmethod
    def process_user_preference(response):
        try:
            user_preference = ast.literal_eval(response)
            columns = [
                "Item Name",
                "Menu ID",
                "Recommendation Date",
                "Average Rating",
                "Meal Type",
                "Recommendation Type",
            ]
            return user_preference, columns
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Error processing recommendations data: {e}")


class UserPreferenceProcessor:
    def __init__(self, client):
        self.data_retriever = DataRetriever(client)
        self.data_processor = DataProcessor()

    def user_preference(self):
        try:
            employee_id = int(input("Enter employee id: "))
            response = self.data_retriever.get_user_preference(employee_id)

            try:
                user_preference, columns = self.data_processor.process_user_preference(
                    response
                )

                DataDisplay.print_info("Preferred food items are : \n")
                for meal_type, rows in user_preference.items():
                    DataDisplay.print_info(f"\n{meal_type} Recommendations:\n")
                    if rows:
                        DataDisplay.print_table(rows, columns)
                    else:
                        DataDisplay.print_no_data("No recommendations available.")
            except ValueError as e:
                DataDisplay.print_error(str(e))

        except Exception as e:
            DataDisplay.print_error(f"Error viewing user preferences: {e}")


class FeedbackRetriever:
    def __init__(self, request):
        self.request = request

    def get_feedback_questions(self):
        return self.request.fetch_feedback_requests()

    def get_user_input(self, prompt):
        return input(prompt)


class FeedbackProcessor:
    @staticmethod
    def process_feedback(question, user_input):
        ques = question.split()
        pattern = r"[a-zA-Z\s]+"
        match = re.match(pattern, ques[-1])
        if match:
            item_name = match.group(0).strip()
            return f"{question}: {user_input}", item_name
        else:
            raise ValueError("Error extracting item name from question.")

class FeedbackHandler:
    def __init__(self, client):
        self.client = client

    def give_feedback(self):
        try:
            FeedbackProcessor(self.client).give_feedback()
        except Exception as e:
            print(Fore.RED + f"❌ Error giving feedback: {e}")

    def view_feedback(self):
        try:
            feedback_str = DataRetriever.get_feedback()
            feedback = DataParser.parse_feedback(feedback_str)
            feedback_formatted = DataParser.format_feedback(feedback)
            DataDisplay.display_feedback(feedback_formatted)
        except Exception as e:
            print(Fore.RED + f"Error viewing feedback: {e}")

    def answer_feedback_questions(self):
        try:
            request = request()
            FeedbackAnswerProcessor(request).answer_feedback_questions()
        except Exception as e:
            print(Fore.RED + f"Error answering feedback questions: {e}")


class FeedbackAnswerProcessor:
    def __init__(self, request):
        self.feedback_retriever = FeedbackRetriever(request)
        self.feedback_processor = FeedbackProcessor()

    def answer_feedback_questions(self):
        try:
            feedback_ques = self.feedback_retriever.get_feedback_questions()

            if feedback_ques:
                user_id = int(self.feedback_retriever.get_user_input("Enter user id: "))
                for iterator, question in enumerate(feedback_ques):
                    DataDisplay.print_warning(
                        f"Question {iterator + 1}: {question[0]}\n"
                    )
                    user_input = self.feedback_retriever.get_user_input(
                        "Answer (type 'exit' to return to main menu): "
                    )

                    if user_input.lower() == "exit":
                        DataDisplay.print_success("\nThanks for your feedback!!\n")
                        self.main_menu()
                        return

                    try:
                        feedback, item_name = self.feedback_processor.process_feedback(
                            question[0], user_input
                        )
                        self.request.user_feedback_request(feedback, user_id, item_name)
                    except ValueError as e:
                        DataDisplay.print_error(str(e))
            else:
                DataDisplay.print_info("No feedback questions available.")
        except Exception as e:
            DataDisplay.print_error(f"Error answering feedback questions: {e}")


class RecommendationRetriever:
    def __init__(self, client):
        self.client = client

    def get_today_recommendations(self):
        response = self.client.send_message("view_today_recommendation")
        return response


class RecommendationProcessor:
    @staticmethod
    def process_recommendations(response):
        try:
            recommendations = ast.literal_eval(response)
            return recommendations
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Error processing recommendations data: {e}")


class RecommendationViewer:
    def __init__(self, client):
        self.retriever = RecommendationRetriever(client)
        self.processor = RecommendationProcessor()

    def view_today_recommendation(self):
        try:
            response = self.retriever.get_today_recommendations()
            try:
                recommendations = self.processor.process_recommendations(response)
                columns = [
                    "menuId",
                    "itemName",
                    "price",
                    "availability Status",
                    "mealType",
                    "recommendationDate",
                ]

                for meal_type, rows in recommendations.items():
                    DataDisplay.print_warning(f"\n{meal_type} Recommendations:\n")
                    if rows:
                        DataDisplay.print_table(rows, columns)
                    else:
                        DataDisplay.print_info("No recommendations available.")
            except ValueError as e:
                DataDisplay.print_error(str(e))
        except Exception as e:
            DataDisplay.print_error(f"Error viewing recommendations: {e}")


class RecommendationsHandler:
    def __init__(self, client):
        self.client = client

    def view_recommendations(self):
        try:
            response = DataRetriever.get_recommendations()
            recommendations = DataParser.parse_recommendations(response)
            recommendations_formatted = DataParser.format_recommendations(recommendations)
            DataDisplay.display_recommendations(recommendations_formatted)
        except Exception as e:
            print(Fore.RED + f"Error viewing recommendations: {e}")

    def view_today_recommendation(self):
        try:
            RecommendationViewer(self.client).view_today_recommendation()
        except Exception as e:
            print(Fore.RED + f"Error viewing today's recommendation: {e}")
            
class ProfileHandler:
    def __init__(self, client):
        self.client = client

    def update_profile(self):
        try:
            profile_processor = ProfileProcessor(self.client, Login())
            profile_processor.update_profile()
        except Exception as e:
            print(Fore.RED + f"Error updating profile: {e}")
            
class PreferenceHandler:
    def __init__(self, client):
        self.client = client

    def user_preference(self):
        try:
            UserPreferenceProcessor(self.client).user_preference()
        except Exception as e:
            print(Fore.RED + f"Error viewing user preferences: {e}")

class OrderHandler:
    def __init__(self, client):
        self.client = client

    def place_order(self):
        try:
            menu_id = int(input("Enter the menu ID (1,2,3 etc..): "))
            user_id = int(input("Enter your user ID: "))
            item_name = input("Enter the Item Name (Idli, Dosa, Biryani etc..): ")
            response = self.client.send_message(f"order|{menu_id}|{user_id}|{item_name}")
            print(Fore.GREEN + f"Order placed successfully for {item_name}!!")
        except Exception as e:
            print(Fore.RED + f"Error placing order: {e}")

class VoteHandler:
    def __init__(self, client):
        self.client = client

    def vote_for_menu_item(self):
        try:
            num_votes = int(input(Fore.YELLOW + "Enter the number of menu items you want to vote for: "))
            for _ in range(num_votes):
                menu_id = int(input(Fore.CYAN + "Enter the menu ID: "))
                response = self.client.send_message(f"vote_for_menu_item|{menu_id}")
                print(Fore.GREEN + response)
        except Exception as e:
            print(Fore.RED + f"Error processing vote: {e}")


