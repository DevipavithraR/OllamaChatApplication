-- MySQL Schema for Hospital AI Appointment Receptionist
CREATE DATABASE IF NOT EXISTS `attendance_db`;
USE `attendance_db`;

-- Departments Table
CREATE TABLE IF NOT EXISTS `departments` (
    `department_id` INT AUTO_INCREMENT PRIMARY KEY,
    `department_name` VARCHAR(100) NOT NULL UNIQUE,
    `description` TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Patients Table
CREATE TABLE IF NOT EXISTS `patients` (
    `patient_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `phone_number` VARCHAR(20) NOT NULL UNIQUE,
    `email` VARCHAR(100) NULL,
    `gender` VARCHAR(10) NULL,
    `age` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_patients_phone` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Doctors Table
CREATE TABLE IF NOT EXISTS `doctors` (
    `doctor_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `department` VARCHAR(100) NOT NULL,
    `specialization` VARCHAR(100) NOT NULL,
    `experience` INT NOT NULL,
    `consultation_fee` DECIMAL(10, 2) NOT NULL,
    `available_days` VARCHAR(100) NOT NULL,
    `available_time` VARCHAR(100) NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_doctors_specialization` (`specialization`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Appointments Table
CREATE TABLE IF NOT EXISTS `appointments` (
    `appointment_id` INT AUTO_INCREMENT PRIMARY KEY,
    `patient_id` INT NOT NULL,
    `doctor_id` INT NOT NULL,
    `appointment_datetime` DATETIME NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    `special_notes` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_appointments_patient` FOREIGN KEY (`patient_id`) 
        REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_appointments_doctor` FOREIGN KEY (`doctor_id`) 
        REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Conversations Table
CREATE TABLE IF NOT EXISTS `conversations` (
    `conversation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(100) NOT NULL UNIQUE,
    `patient_id` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_conversations_patient` FOREIGN KEY (`patient_id`) 
        REFERENCES `patients` (`patient_id`) ON DELETE SET NULL
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
INSERT INTO `departments` (`department_name`, `description`) VALUES
('Cardiology', 'Heart related diagnosis and treatment.'),
('Pediatrics', 'Child healthcare.'),
('Orthopedics', 'Bone and joint treatment.'),
('Neurology', 'Brain and nervous system.'),
('General Medicine', 'General healthcare.');

-- Seed Doctors Data
INSERT INTO `doctors` (`name`, `department`, `specialization`, `experience`, `consultation_fee`, `available_days`, `available_time`, `status`) VALUES
('Dr. Priya', 'Cardiology', 'Cardiologist', 12, 700.00, 'Monday-Friday', '10 AM-4 PM', 'ACTIVE'),
('Dr. Sharma', 'Pediatrics', 'Pediatrician', 8, 500.00, 'Monday-Saturday', '9 AM-1 PM', 'ACTIVE'),
('Dr. Goel', 'Orthopedics', 'Orthopedic Surgeon', 15, 800.00, 'Tuesday-Thursday-Saturday', '2 PM-6 PM', 'ACTIVE'),
('Dr. Gupta', 'Neurology', 'Neurologist', 10, 900.00, 'Monday-Wednesday-Friday', '11 AM-5 PM', 'ACTIVE'),
('Dr. Verma', 'General Medicine', 'General Physician', 6, 400.00, 'Monday-Saturday', '9 AM-5 PM', 'ACTIVE');
