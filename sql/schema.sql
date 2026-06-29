-- MySQL Schema for Movie Ticket Booking Assistant
CREATE DATABASE IF NOT EXISTS `ticket_db`;
USE `ticket_db`;

-- Customers Table
CREATE TABLE IF NOT EXISTS `customers` (
    `customer_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `phone_number` VARCHAR(20) NOT NULL UNIQUE,
    `email` VARCHAR(100) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_customers_phone` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Movies Table
CREATE TABLE IF NOT EXISTS `movies` (
    `movie_id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL UNIQUE,
    `genre` VARCHAR(100) NOT NULL,
    `language` VARCHAR(50) NOT NULL,
    `duration` VARCHAR(50) NOT NULL,
    `rating` VARCHAR(10) NOT NULL,
    `description` TEXT NULL,
    `release_date` DATE NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Theatres Table
CREATE TABLE IF NOT EXISTS `theatres` (
    `theatre_id` INT AUTO_INCREMENT PRIMARY KEY,
    `theatre_name` VARCHAR(100) NOT NULL UNIQUE,
    `location` VARCHAR(255) NOT NULL,
    `screens` INT NOT NULL DEFAULT 1,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Shows Table
CREATE TABLE IF NOT EXISTS `shows` (
    `show_id` INT AUTO_INCREMENT PRIMARY KEY,
    `movie_id` INT NOT NULL,
    `theatre_id` INT NOT NULL,
    `screen_number` INT NOT NULL,
    `show_datetime` DATETIME NOT NULL,
    `ticket_price` DECIMAL(10, 2) NOT NULL,
    `available_seats` INT NOT NULL,
    `total_seats` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_shows_movie` FOREIGN KEY (`movie_id`) 
        REFERENCES `movies` (`movie_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_shows_theatre` FOREIGN KEY (`theatre_id`) 
        REFERENCES `theatres` (`theatre_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bookings Table
CREATE TABLE IF NOT EXISTS `bookings` (
    `booking_id` INT AUTO_INCREMENT PRIMARY KEY,
    `customer_id` INT NOT NULL,
    `show_id` INT NOT NULL,
    `seat_numbers` TEXT NOT NULL,
    `number_of_tickets` INT NOT NULL,
    `total_amount` DECIMAL(10, 2) NOT NULL,
    `booking_status` VARCHAR(50) NOT NULL DEFAULT 'Confirmed', -- Confirmed, Cancelled, Modified
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_bookings_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`customer_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_bookings_show` FOREIGN KEY (`show_id`) 
        REFERENCES `shows` (`show_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Conversations Table
CREATE TABLE IF NOT EXISTS `conversations` (
    `conversation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(100) NOT NULL UNIQUE,
    `customer_id` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_conversations_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`customer_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Messages Table
CREATE TABLE IF NOT EXISTS `messages` (
    `message_id` INT AUTO_INCREMENT PRIMARY KEY,
    `conversation_id` INT NOT NULL,
    `sender` VARCHAR(20) NOT NULL, -- 'user' or 'bot'
    `message` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_messages_conversation` FOREIGN KEY (`conversation_id`) 
        REFERENCES `conversations` (`conversation_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed Movies Data
INSERT INTO `movies` (`title`, `genre`, `language`, `duration`, `rating`, `description`, `release_date`) VALUES
('Interstellar', 'Sci-Fi', 'English', '169 Minutes', 'PG-13', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.', '2014-11-07'),
('Inception', 'Sci-Fi', 'English', '148 Minutes', 'PG-13', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.', '2010-07-16'),
('The Dark Knight', 'Action', 'English', '152 Minutes', 'PG-13', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.', '2008-07-18');

-- Seed Theatres Data
INSERT INTO `theatres` (`theatre_name`, `location`, `screens`) VALUES
('PVR Cinemas', 'Mall of India, Sector 18', 4),
('IMAX Theatre', 'Forum Mall, Koramangala', 2);

-- Seed Shows Data
INSERT INTO `shows` (`movie_id`, `theatre_id`, `screen_number`, `show_datetime`, `ticket_price`, `available_seats`, `total_seats`) VALUES
(1, 1, 2, '2026-07-20 19:30:00', 250.00, 42, 50),
(2, 1, 1, '2026-07-20 14:00:00', 200.00, 50, 50),
(1, 2, 1, '2026-07-21 18:00:00', 400.00, 35, 40);
