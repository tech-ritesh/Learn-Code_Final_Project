from Database.connection import DatabaseConnection
from tabulate import tabulate


class Voting:
    def __init__(self, menuId=None) -> None:
        self.menuId = menuId
        self.connect = DatabaseConnection().get_connection().cursor()

    def vote_for_menu_item(self, menuId=None):

        if menuId is None:
            return
        else:
            try:
                self.connect.execute("INSERT INTO Votes (menuId) VALUES (?)", (menuId,))
                self.connect.commit()
            except Exception as e:
                return f"Error voting for menu item: {e}"
            finally:
                self.connect.close()

    def view_employee_votes(self):

        try:
            query = """
            SELECT m.Id, m.itemName, COUNT(v.voteId) AS voteCount
            FROM Votes v
            JOIN Menu m ON v.menuId = m.Id
            GROUP BY m.Id, m.itemName
            ORDER BY voteCount DESC
            """
            self.connect.execute(query)
            rows = self.connect.fetchall()
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
            self.connect.close()
