-- MySQL Schema for Restaurant Receptionist AI Chatbot
CREATE DATABASE IF NOT EXISTS `restaurant_db`;
USE `restaurant_db`;

-- Customers Table
CREATE TABLE IF NOT EXISTS `customers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `phone` VARCHAR(20) NOT NULL UNIQUE,
    `email` VARCHAR(100) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_customers_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reservations Table
CREATE TABLE IF NOT EXISTS `reservations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `customer_id` INT NOT NULL,
    `reservation_time` DATETIME NOT NULL,
    `party_size` INT NOT NULL,
    `special_requests` TEXT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_reservations_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Menu Items Table
CREATE TABLE IF NOT EXISTS `menu_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `is_available` BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX `idx_menu_category` (`category`),
    FULLTEXT INDEX `idx_menu_search` (`name`, `description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Conversations Table
CREATE TABLE IF NOT EXISTS `conversations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(100) NOT NULL UNIQUE,
    `customer_id` INT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_conversations_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Messages Table (stores conversation history)
CREATE TABLE IF NOT EXISTS `messages` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `conversation_id` INT NOT NULL,
    `sender` VARCHAR(20) NOT NULL, -- 'user' or 'bot'
    `content` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_messages_conversation` FOREIGN KEY (`conversation_id`) 
        REFERENCES `conversations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed Sample Menu Data
INSERT INTO `menu_items` (`name`, `description`, `price`, `category`, `is_available`) VALUES
('Caprese Salad', 'Fresh mozzarella, ripe tomatoes, sweet basil leaves, drizzled with balsamic glaze and extra virgin olive oil.', 11.50, 'appetizers', 1),
('Bruschetta', 'Grilled bread rubbed with garlic, topped with diced tomatoes, fresh basil, and extra virgin olive oil.', 9.00, 'appetizers', 1),
('Minestrone Soup', 'Classic Italian vegetable soup made with tomatoes, beans, onions, celery, carrots, and pasta.', 8.50, 'appetizers', 1),
('Margherita Pizza', 'Traditional Italian pizza topped with tomato sauce, fresh mozzarella, and sweet basil.', 14.50, 'entrees', 1),
('Fettuccine Alfredo', 'Fettuccine pasta tossed in a rich, creamy sauce made of parmesan cheese and butter.', 17.50, 'entrees', 1),
('Spaghetti Carbonara', 'Spaghetti tossed with crispy pancetta, eggs, pecorino romano cheese, and cracked black pepper.', 18.00, 'entrees', 1),
('Grilled Ribeye Steak', 'Premium ribeye steak grilled to order, served with garlic mashed potatoes and roasted asparagus.', 32.00, 'entrees', 1),
('Chicken Parmigiana', 'Breaded chicken breast baked with tomato sauce and mozzarella cheese, served over spaghetti.', 21.00, 'entrees', 1),
('Tiramisu', 'Classic Italian dessert made of coffee-dipped ladyfingers layered with whipped mascarpone cheese and cocoa.', 8.50, 'desserts', 1),
('Panna Cotta', 'Creamy Italian pudding sweetened with sugar and vanilla, topped with a fresh raspberry coulis.', 7.50, 'desserts', 1),
('Gelato Trio', 'Three scoops of authentic Italian gelato. Flavors: dark chocolate, pistachio, and Tahitian vanilla.', 6.50, 'desserts', 1),
('Chardonnay', 'Crisp white wine with notes of apple, pear, and a touch of oak. Glass/Bottle.', 9.50, 'drinks', 1),
('Chianti Classico', 'Bold red wine with cherry, leather, and vanilla tasting notes. Glass/Bottle.', 11.00, 'drinks', 1),
('San Pellegrino', 'Sparkling natural mineral water from the Italian Alps.', 4.50, 'drinks', 1),
('Espresso', 'Rich and intense shot of freshly brewed espresso.', 3.50, 'drinks', 1);
