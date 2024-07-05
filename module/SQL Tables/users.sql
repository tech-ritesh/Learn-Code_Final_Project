CREATE TABLE users (
    employeeId INT PRIMARY KEY,
    name VARCHAR(250),
    role VARCHAR(250)
);

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

CREATE TABLE Recommendations (
    RecommendationId INT IDENTITY(1,1) PRIMARY KEY,
    menuId INT,
    recommendationDate DATETIME,
    itemName VARCHAR(250),
    mealType VARCHAR(250),
    CONSTRAINT FK_MenuId FOREIGN KEY (menuId) REFERENCES menu(id)
);

CREATE TABLE Notification (
    notificationId INT IDENTITY(1,1) PRIMARY KEY,
    message VARCHAR(250),
    date_of_notification DATETIME
);

CREATE TABLE discard_feedback (
    id INT IDENTITY(1,1) PRIMARY KEY,
    feedback_request VARCHAR(250)
);

