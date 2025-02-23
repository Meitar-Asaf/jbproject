DROP DATABASE IF EXISTS vacation_website_database;
CREATE DATABASE vacation_website_database;
USE vacation_website_database;
CREATE TABLE roles(role_id SERIAL PRIMARY KEY, role_name UNIQUE VARCHAR(6));
CREATE TABLE users(user_id SERIAL PRIMARY KEY, first_name VARCHAR(20), last_name VARCHAR(20), email UNIQUE NOT NULL, password NOT NULL VARCHAR(20), role_id FOREIGN KEY REFERENCES roles(role_id));
CREATE TABLE countries(country_id INT PRIMARY KEY, country_name UNIQUE NOT NULL VARCHAR(50));
CREATE TABLE