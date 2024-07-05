CREATE TABLE Recommendations (
    RecommendationId INT IDENTITY(1,1) PRIMARY KEY,
    menuId INT,
    recommendationDate DATETIME,
    itemName VARCHAR(250),
    mealType VARCHAR(250),
    CONSTRAINT FK_MenuId FOREIGN KEY (menuId) REFERENCES menu(id)
);

