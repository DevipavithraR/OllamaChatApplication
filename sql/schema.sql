-- MySQL Schema for AI Vehicle Service Center Assistant
CREATE DATABASE IF NOT EXISTS `vehicle_db`;
USE `vehicle_db`;

-- 1. Customers Table
CREATE TABLE IF NOT EXISTS `customers` (
    `customer_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `phone_number` VARCHAR(20) NOT NULL UNIQUE,
    `email` VARCHAR(100) NULL,
    `address` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_customers_phone` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Vehicles Table
CREATE TABLE IF NOT EXISTS `vehicles` (
    `vehicle_id` INT AUTO_INCREMENT PRIMARY KEY,
    `customer_id` INT NOT NULL,
    `vehicle_number` VARCHAR(20) NOT NULL UNIQUE,
    `vehicle_brand` VARCHAR(50) NOT NULL,
    `vehicle_model` VARCHAR(50) NOT NULL,
    `fuel_type` VARCHAR(20) NOT NULL,
    `manufacturing_year` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_vehicles_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`customer_id`) ON DELETE CASCADE,
    INDEX `idx_vehicles_number` (`vehicle_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Mechanics Table
CREATE TABLE IF NOT EXISTS `mechanics` (
    `mechanic_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `specialization` VARCHAR(100) NOT NULL,
    `experience` INT NOT NULL,
    `available_status` VARCHAR(20) NOT NULL DEFAULT 'Available',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Service Catalog Table
CREATE TABLE IF NOT EXISTS `service_catalog` (
    `service_id` INT AUTO_INCREMENT PRIMARY KEY,
    `service_name` VARCHAR(100) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `estimated_duration` VARCHAR(50) NOT NULL, -- e.g. '2 Hours'
    `service_cost` DECIMAL(10, 2) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FULLTEXT INDEX `idx_service_search` (`service_name`, `description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Service Bookings Table
CREATE TABLE IF NOT EXISTS `service_bookings` (
    `booking_id` INT AUTO_INCREMENT PRIMARY KEY,
    `customer_id` INT NOT NULL,
    `vehicle_id` INT NOT NULL,
    `mechanic_id` INT NULL,
    `service_id` INT NOT NULL,
    `service_date` DATETIME NOT NULL,
    `booking_status` VARCHAR(20) NOT NULL DEFAULT 'Scheduled',
    `estimated_completion` DATETIME NULL,
    `customer_notes` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_bookings_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`customer_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_bookings_vehicle` FOREIGN KEY (`vehicle_id`) 
        REFERENCES `vehicles` (`vehicle_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_bookings_mechanic` FOREIGN KEY (`mechanic_id`) 
        REFERENCES `mechanics` (`mechanic_id`) ON DELETE SET NULL,
    CONSTRAINT `fk_bookings_service` FOREIGN KEY (`service_id`) 
        REFERENCES `service_catalog` (`service_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Conversations Table
CREATE TABLE IF NOT EXISTS `conversations` (
    `conversation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(100) NOT NULL UNIQUE,
    `customer_id` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_conversations_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`customer_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Messages Table
CREATE TABLE IF NOT EXISTS `messages` (
    `message_id` INT AUTO_INCREMENT PRIMARY KEY,
    `conversation_id` INT NOT NULL,
    `sender` VARCHAR(20) NOT NULL, -- 'user' or 'bot'
    `message` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_messages_conversation` FOREIGN KEY (`conversation_id`) 
        REFERENCES `conversations` (`conversation_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed Service Catalog
INSERT INTO `service_catalog` (`service_name`, `description`, `estimated_duration`, `service_cost`) VALUES
('General Service', 'Complete vehicle inspection, engine oil check & top up, filter cleaning, and basic electrical check.', '2 Hours', 2500.00),
('Engine Repair', 'Advanced engine diagnostics, cylinder block overhaul, timing belt adjustments, and valve tuning.', '6 Hours', 8500.00),
('Brake Replacement', 'Front and rear brake pad replacement, disc brake resurfacing, and brake fluid flushing.', '1.5 Hours', 1800.00),
('AC Overhaul', 'AC compressor testing, condenser wash, evaporator cleaning, and refrigerant gas top-up.', '3 Hours', 3000.00),
('Wheel Alignment', 'Precision wheel alignment, high-speed wheel balancing, tyre rotation, and tread health inspection.', '1 Hour', 1200.00);

-- Seed Mechanics
INSERT INTO `mechanics` (`name`, `specialization`, `experience`, `available_status`) VALUES
('Arun Kumar', 'Engine Repair', 10, 'Available'),
('Rajesh Sharma', 'Brake Replacement', 8, 'Available'),
('Vikram Singh', 'AC Overhaul', 6, 'Available'),
('Amit Patel', 'Wheel Alignment', 4, 'Available'),
('Senthil Kumar', 'General Service', 5, 'Available');
