CREATE DATABASE IF NOT EXISTS `mydatabase`;

USE `mydatabase`;

CREATE TABLE IF NOT EXISTS `tweets` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `text` TEXT NOT NULL,
    `positive` INT(1) NOT NULL DEFAULT 0,
    `negative` INT(1) NOT NULL DEFAULT 0
);