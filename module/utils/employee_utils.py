from colorama import Fore, Style
from tabulate import tabulate
import ast
import re


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
