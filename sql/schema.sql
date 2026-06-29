-- MySQL Schema for Library Management AI Chatbot
CREATE DATABASE IF NOT EXISTS `library_db`;
USE `library_db`;

-- Members Table
CREATE TABLE IF NOT EXISTS `members` (
    `member_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `phone_number` VARCHAR(20) NOT NULL UNIQUE,
    `email` VARCHAR(100) NULL,
    `membership_type` VARCHAR(50) NOT NULL DEFAULT 'Regular',
    `registration_date` DATE NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_members_phone` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Books Table
CREATE TABLE IF NOT EXISTS `books` (
    `book_id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `author` VARCHAR(100) NOT NULL,
    `category` VARCHAR(100) NOT NULL,
    `isbn` VARCHAR(20) NOT NULL UNIQUE,
    `publisher` VARCHAR(100) NOT NULL,
    `publication_year` INT NOT NULL,
    `available_copies` INT NOT NULL,
    `total_copies` INT NOT NULL,
    `description` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_books_category` (`category`),
    FULLTEXT INDEX `idx_books_search` (`title`, `author`, `description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- IssuedBooks Table
CREATE TABLE IF NOT EXISTS `issued_books` (
    `issue_id` INT AUTO_INCREMENT PRIMARY KEY,
    `member_id` INT NOT NULL,
    `book_id` INT NOT NULL,
    `issue_date` DATE NOT NULL,
    `due_date` DATE NOT NULL,
    `return_date` DATE NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'Issued', -- 'Issued', 'Returned'
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_issued_books_member` FOREIGN KEY (`member_id`) 
        REFERENCES `members` (`member_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_issued_books_book` FOREIGN KEY (`book_id`) 
        REFERENCES `books` (`book_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Conversations Table
CREATE TABLE IF NOT EXISTS `conversations` (
    `conversation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(100) NOT NULL UNIQUE,
    `member_id` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_conversations_member` FOREIGN KEY (`member_id`) 
        REFERENCES `members` (`member_id`) ON DELETE SET NULL
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

-- Seed Sample Books Data
INSERT INTO `books` (`title`, `author`, `category`, `isbn`, `publisher`, `publication_year`, `available_copies`, `total_copies`, `description`) VALUES
('Clean Code', 'Robert C. Martin', 'Programming', '978-0132350884', 'Prentice Hall', 2008, 5, 5, 'A handbook of agile software craftsmanship. Master the art of clean code.'),
('Introduction to Algorithms', 'Thomas H. Cormen', 'Computer Science', '978-0262033848', 'MIT Press', 2009, 3, 3, 'A comprehensive design and analysis guide for algorithms.'),
('Design Patterns', 'Erich Gamma', 'Programming', '978-0201633610', 'Addison-Wesley', 1994, 4, 4, 'Elements of Reusable Object-Oriented Software. The classic software engineering text.'),
('The Pragmatic Programmer', 'Andrew Hunt', 'Programming', '978-0135957059', 'Addison-Wesley', 2019, 6, 6, 'Your journey to mastery. From journeyman to master.'),
('Artificial Intelligence: A Modern Approach', 'Stuart Russell', 'AI/ML', '978-0136042594', 'Pearson', 2020, 2, 2, 'The reference textbook for AI studies worldwide.');

-- Seed Sample Members Data
INSERT INTO `members` (`name`, `phone_number`, `email`, `membership_type`, `registration_date`) VALUES
('Rahul Kumar', '+919876543210', 'rahul@example.com', 'Premium', '2026-06-01'),
('Alice Smith', '+15550199', 'alice@example.com', 'Regular', '2026-06-15');
