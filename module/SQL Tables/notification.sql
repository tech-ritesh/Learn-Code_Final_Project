CREATE TABLE Notification (
    notificationId INT IDENTITY(1,1) PRIMARY KEY,
    message VARCHAR(250),
    date_of_notification DATETIME
);

CREATE TABLE discard_feedback (
    id INT IDENTITY(1,1) PRIMARY KEY,
    feedback_request VARCHAR(250)
);