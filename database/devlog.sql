CREATE DATABASE IF NOT EXISTS devlog;
USE devlog;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    username VARCHAR(50),
    password VARCHAR(255)
);

CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(50),
    category VARCHAR(50),
    content TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);