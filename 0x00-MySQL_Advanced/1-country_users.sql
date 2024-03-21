-- SQL script to create a table named 'users'

-- Ensure the existence of the table or create it if absent
CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each user
	email VARCHAR(255) NOT NULL UNIQUE, -- Email address of the user (must be unique)
	name VARCHAR(255), -- Name of the user
	country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL -- Country of the user with default value 'US' (United States)
);
