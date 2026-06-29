-- MySQL Schema for Gym Receptionist and Membership Management System AI
CREATE DATABASE IF NOT EXISTS `gym_db`;
USE `gym_db`;

-- Members Table
CREATE TABLE IF NOT EXISTS `members` (
    `member_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `phone_number` VARCHAR(20) NOT NULL UNIQUE,
    `email` VARCHAR(100) NULL,
    `gender` VARCHAR(10) NULL,
    `age` INT NULL,
    `membership_status` VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_members_phone` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- MembershipPlans Table
CREATE TABLE IF NOT EXISTS `membership_plans` (
    `plan_id` INT AUTO_INCREMENT PRIMARY KEY,
    `plan_name` VARCHAR(100) NOT NULL UNIQUE,
    `duration` VARCHAR(50) NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    `benefits` TEXT NULL,
    `description` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_plans_name` (`plan_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Trainers Table
CREATE TABLE IF NOT EXISTS `trainers` (
    `trainer_id` INT AUTO_INCREMENT PRIMARY KEY,
    `trainer_name` VARCHAR(100) NOT NULL UNIQUE,
    `specialization` VARCHAR(200) NOT NULL,
    `experience` VARCHAR(50) NOT NULL,
    `available_days` VARCHAR(100) NOT NULL,
    `available_time` VARCHAR(100) NOT NULL,
    `session_fee` DECIMAL(10, 2) NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_trainers_name` (`trainer_name`),
    FULLTEXT INDEX `idx_trainers_search` (`trainer_name`, `specialization`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TrainerBookings Table
CREATE TABLE IF NOT EXISTS `trainer_bookings` (
    `booking_id` INT AUTO_INCREMENT PRIMARY KEY,
    `member_id` INT NOT NULL,
    `trainer_id` INT NOT NULL,
    `booking_datetime` DATETIME NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    `training_goal` VARCHAR(200) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_bookings_member` FOREIGN KEY (`member_id`) 
        REFERENCES `members` (`member_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_bookings_trainer` FOREIGN KEY (`trainer_id`) 
        REFERENCES `trainers` (`trainer_id`) ON DELETE CASCADE
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

-- Seed Sample Membership Plans
INSERT INTO `membership_plans` (`plan_name`, `duration`, `price`, `benefits`, `description`) VALUES
('Gold Membership', '12 Months', 18000.00, 'Unlimited Gym Access, Personal Diet Plan, Group Classes', 'All-access premium pass to the gym and group activities.'),
('Silver Membership', '6 Months', 10000.00, 'Unlimited Gym Access, Group Classes', 'Standard pass covering basic facilities and group workouts.'),
('Platinum Membership', '12 Months', 25000.00, 'Unlimited Gym Access, Personal Diet Plan, Group Classes, 1-on-1 Personal Trainer', 'Ultimate pass with full training support and personalized guidance.')
ON DUPLICATE KEY UPDATE `price` = VALUES(`price`);

-- Seed Sample Trainers
INSERT INTO `trainers` (`trainer_name`, `specialization`, `experience`, `available_days`, `available_time`, `session_fee`, `status`) VALUES
('Rahul Sharma', 'Weight Loss, Strength Training', '8 Years', 'Monday-Friday', '6:00 AM - 2:00 PM', 600.00, 'ACTIVE'),
('Priya Patel', 'Yoga, Pilates, Flexibility', '5 Years', 'Monday-Saturday', '7:00 AM - 12:00 PM', 500.00, 'ACTIVE'),
('Vikram Singh', 'Bodybuilding, Strength & Conditioning', '10 Years', 'Monday, Wednesday, Friday', '2:00 PM - 8:00 PM', 800.00, 'ACTIVE')
ON DUPLICATE KEY UPDATE `session_fee` = VALUES(`session_fee`);
