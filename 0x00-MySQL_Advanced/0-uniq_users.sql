-- Create a table 'users' if it doesn't exist

-- Check if the table 'users' exists, if not, create it
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each user
    email VARCHAR(255) NOT NULL UNIQUE, -- Email address of the user
    name VARCHAR(255) -- Name of the user
);
