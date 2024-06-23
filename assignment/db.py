
import pyodbc as odbccon

def get_connection():
    conn = odbccon.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=(local)\SQLEXPRESS;'
    r'DATABASE=Cafeteria;'
    r'Trusted_Connection=yes;'
)
    # cur1 = conn.cursor()
    return conn

# CREATE DATABASE cafeteria;

# USE cafeteria;

# CREATE TABLE Users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     employeeId VARCHAR(100) NOT NULL,
#     name VARCHAR(100) NOT NULL,
#     role ENUM('Admin', 'Chef', 'Employee') NOT NULL
# );

# CREATE TABLE Menu (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     itemName VARCHAR(255) NOT NULL,
#     price DECIMAL(10, 2) NOT NULL,
#     availability_status ENUM('Available', 'Unavailable') NOT NULL DEFAULT 'Available'
# );

# CREATE TABLE Feedback (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     userId INT NOT NULL,
#     menuId INT NOT NULL,
#     rating INT CHECK (rating >= 1 AND rating <= 5),
#     comment TEXT,
#     feedbackDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (userId) REFERENCES Users(id),
#     FOREIGN KEY (menuId) REFERENCES Menu(id)
# );

# CREATE TABLE Recommendations (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     menuId INT NOT NULL,
#     recommendationDate DATE NOT NULL,
#     FOREIGN KEY (menuId) REFERENCES Menu(id)
# );
