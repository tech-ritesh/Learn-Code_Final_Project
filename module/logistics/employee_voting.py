from Database import connection
from tabulate import tabulate


class Voting:
    def __init__(self, menuId=None) -> None:
        self.menuId = menuId

    def vote_for_menu_item(self, menuId=None):

        if menuId is None:
            return
        else:
            cursor = connection.get_connection().cursor()
            try:
                cursor.execute("INSERT INTO Votes (menuId) VALUES (?)", (menuId,))
                cursor.commit()
            except Exception as e:
                return f"Error voting for menu item: {e}"
            finally:
                cursor.close()

    def view_employee_votes(self):

        try:
            cursor = connection.get_connection().cursor()
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
                table = tabulate(
                    rows,
                    headers=["Menu ID", "Item Name", "Vote Count"],
                    tablefmt="grid",
                )
                return table
            else:
                return "No votes found."
        except Exception as e:
            return f"Error retrieving votes: {e}"
        finally:
            cursor.close()
