CREATE TABLE users(
    ID SERIAL PRIMARY KEY,
    Fullname TEXT NOT NULL,
    Email TEXT NOT NULL,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    Salt TEXT NOT NULL,
    LastLogin TIMESTAMP DEFAULT NULL
);

CREATE TABLE musicsettings(
    Username TEXT NOT NULL,
    NumSearches INT DEFAULT 10
);
