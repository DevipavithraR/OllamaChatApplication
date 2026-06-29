-- MySQL Schema for College Admission Assistant
CREATE DATABASE IF NOT EXISTS `college_db`;
USE `college_db`;

-- Departments Table
CREATE TABLE IF NOT EXISTS `departments` (
    `department_id` INT AUTO_INCREMENT PRIMARY KEY,
    `department_name` VARCHAR(100) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `head_of_department` VARCHAR(100) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Students Table
CREATE TABLE IF NOT EXISTS `students` (
    `student_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `phone_number` VARCHAR(20) NOT NULL UNIQUE,
    `email` VARCHAR(100) NULL,
    `date_of_birth` DATE NULL,
    `gender` VARCHAR(10) NULL,
    `address` TEXT NULL,
    `marks_percentage` DECIMAL(5, 2) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_students_phone` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Courses Table
CREATE TABLE IF NOT EXISTS `courses` (
    `course_id` INT AUTO_INCREMENT PRIMARY KEY,
    `course_name` VARCHAR(100) NOT NULL UNIQUE,
    `department_id` INT NOT NULL,
    `duration` VARCHAR(50) NOT NULL,
    `total_seats` INT NOT NULL,
    `available_seats` INT NOT NULL,
    `fees` DECIMAL(10, 2) NOT NULL,
    `eligibility` TEXT NOT NULL,
    `description` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_courses_department` FOREIGN KEY (`department_id`) 
        REFERENCES `departments` (`department_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Admissions Table
CREATE TABLE IF NOT EXISTS `admissions` (
    `admission_id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `course_id` INT NOT NULL,
    `application_date` DATE NOT NULL,
    `status` VARCHAR(50) NOT NULL DEFAULT 'Pending Verification',
    `remarks` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_admissions_student` FOREIGN KEY (`student_id`) 
        REFERENCES `students` (`student_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_admissions_course` FOREIGN KEY (`course_id`) 
        REFERENCES `courses` (`course_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Conversations Table
CREATE TABLE IF NOT EXISTS `conversations` (
    `conversation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(100) NOT NULL UNIQUE,
    `student_id` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_conversations_student` FOREIGN KEY (`student_id`) 
        REFERENCES `students` (`student_id`) ON DELETE SET NULL
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

-- Seed Departments Data
INSERT INTO `departments` (`department_name`, `description`, `head_of_department`) VALUES
('Computer Science Department', 'Focuses on AI, Cloud Computing, Software Development and Data Science.', 'Dr. Alan Turing'),
('Electronics & Communication Department', 'Covers core hardware, embedded devices, and communication networks.', 'Dr. Claude Shannon'),
('Information Technology Department', 'Studies web development, software engineering, databases, and networks.', 'Dr. Tim Berners-Lee'),
('Mechanical Engineering Department', 'Deals with designs, thermal engineering, robotics, and production.', 'Dr. James Watt');

-- Seed Courses Data
INSERT INTO `courses` (`course_name`, `department_id`, `duration`, `total_seats`, `available_seats`, `fees`, `eligibility`, `description`) VALUES
('B.Tech Computer Science', 1, '4 Years', 30, 25, 85000.00, 'Minimum 60%', 'Focuses on core programming, machine learning, systems architecture and algorithmic theory.'),
('B.Tech Data Science', 1, '4 Years', 25, 22, 90000.00, 'Minimum 65%', 'Learn modern big data ingestion, statistics, data analytics and machine learning.'),
('B.Tech Electronics & Comm.', 2, '4 Years', 20, 18, 80000.00, 'Minimum 55%', 'Comprehensive study of semiconductor devices, RF communication, VLSI, and signal processing.'),
('M.Tech Software Engineering', 3, '2 Years', 15, 12, 110000.00, 'Minimum 65%', 'Advanced system architecture, software quality controls, DevOps, and project management.');
