CREATE DATABASE wedlockwonders;

USE wedlockwonders;

CREATE TABLE users (
    user_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE venues (
    venue_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    capacity INT(11) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE catering (
    catering_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE decorations (
    decoration_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE orchestra (
    orchestra_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE bookings (
    booking_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) NOT NULL,
    venue_id INT(11) NOT NULL,
    catering_id INT(11),
    orchestra_id INT(11),
    decoration_id INT(11),
    booking_date DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (catering_id) REFERENCES catering(catering_id),
    FOREIGN KEY (orchestra_id) REFERENCES orchestra(orchestra_id),
    FOREIGN KEY (decoration_id) REFERENCES decorations(decoration_id)
);
