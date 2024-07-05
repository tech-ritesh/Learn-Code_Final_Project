CREATE TABLE Notification (
    notificationId INT IDENTITY(1,1) PRIMARY KEY,
    message VARCHAR(250),
    date_of_notification DATETIME
);

