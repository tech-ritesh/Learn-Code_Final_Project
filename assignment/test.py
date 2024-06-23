import pyodbc as odbccon

# conn = odbccon.connect(
#     r'DRIVER={SQL Server};'
#     r'SERVER=(local)\SQLEXPRESS;'
#     r'DATABASE=Cafeteria;'
#     r'Trusted_Connection=yes;'
# )
# cur1 = conn.cursor()
# sql = "INSERT INTO Menu (itemName, price, availabilityStatus) VALUES (?, ?, ?)"
# item_name = input("Enter item name: ")
# price = float(input("Enter item price: "))
# availabilityStatus = int(input("Enter the availabilityStatus: "))
# cur1.execute(sql, (item_name, price, availabilityStatus))
# cur1.commit()

# cur1.execute("select * from Menu")
# result = cur1.fetchall()
# # for i in cur1:
# print(result)

# from datetime import datetime

# a = datetime.now().strftime("%y-%m-%d")

conn = odbccon.connect(
        r'DRIVER={SQL Server};'
        r'SERVER=(local)\SQLEXPRESS;'
        r'DATABASE=Cafeteria;'
        r'Trusted_Connection=yes;'
    )
cur1 = conn.cursor()
sql = """SELECT menuId ,itemName, mealType
FROM Recommendations"""
cur1.execute(sql)
result = cur1.fetchall()
print(result)