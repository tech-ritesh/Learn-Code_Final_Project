CREATE TABLE Feedback (
    id INT IDENTITY(1,1) PRIMARY KEY,
    userId INT,
    menuId INT,
    rating INT,
    comment VARCHAR(250),
    feedbackDate DATETIME,
    CONSTRAINT FK_UserId FOREIGN KEY (userId) REFERENCES users(employeeId),
    CONSTRAINT FK_MenuId FOREIGN KEY (menuId) REFERENCES menu(id)
);



