-- Drop tables if they exist
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS commands;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create messages table (for XSS demo)
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create files table (for directory traversal demo)
CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create commands table (for command injection demo)
CREATE TABLE commands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    command VARCHAR(255) NOT NULL,
    output TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data for users
INSERT INTO users (username, password, email, role) VALUES 
('admin', 'admin123', 'admin@example.com', 'admin'),
('user1', 'password123', 'user1@example.com', 'user'),
('user2', 'abcd1234', 'user2@example.com', 'user');

-- Insert sample data for messages
INSERT INTO messages (user_id, content) VALUES 
(1, 'Welcome to the Attack Mitigation Tool!'),
(2, 'Hello everyone, this is a test message.'),
(3, 'Learning about cybersecurity is fun!');

-- Insert sample data for files
INSERT INTO files (filename, path, content) VALUES 
('welcome.txt', '/public/files/', 'Welcome to our application!'),
('notes.txt', '/public/files/', 'These are some public notes.'),
('secret.txt', '/private/files/', 'This is a secret file that should not be accessible.');

-- Insert sample data for commands
INSERT INTO commands (command, output) VALUES 
('ls -la', 'Directory listing output'),
('echo "Hello"', 'Hello'),
('date', 'Current date output');