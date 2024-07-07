CREATE TABLE menu (
    id INT IDENTITY(1,1) PRIMARY KEY,
    itemName VARCHAR(250),
    price INT,
    availabilityStatus BIT,
    mealType VARCHAR(250),
    speciality VARCHAR(250),
    is_deleted BIT,
    dietary_preference VARCHAR(250),
    spice_level VARCHAR(250),
    preferred_cuisine VARCHAR(250),
    sweet_tooth VARCHAR(250)
);

