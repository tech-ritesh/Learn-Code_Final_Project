from Database import connection
from tabulate import tabulate

class Voting:
    def __init__(self, menuId=None) -> None:
        self.menuId = menuId

    def vote_for_menu_item(self, menuId=None):
        if menuId is None:
            menuId = self.menuId

        if menuId is None:
            print("No menuId provided.")
            return

        cursor = connection.get_connection().cursor()
        try:
            cursor.execute("INSERT INTO Votes (menuId) VALUES (?)", (menuId,))
            cursor.commit()
            print(f"Successfully voted for menu item {menuId}")
        except Exception as e:
            print(f"Error voting for menu item: {e}")
        finally:
            cursor.close()

    def view_employee_votes(self):
        cursor = connection.get_connection().cursor()
        try:
            query = """
            SELECT m.Id, m.itemName, COUNT(v.voteId) AS voteCount
            FROM Votes v
            JOIN Menu m ON v.menuId = m.Id
            GROUP BY m.Id, m.itemName
            ORDER BY voteCount DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                table = tabulate(rows, headers=["Menu ID", "Item Name", "Vote Count"], tablefmt="grid")
                return table
            else:
                return "No votes found."
        except Exception as e:
            return f"Error retrieving votes: {e}"
        finally:
            cursor.close()
