DROP DATABASE IF EXISTS vacation_website_database;
CREATE DATABASE vacation_website_database;
-- User should connect to the vacation_website_database before running the following commands
CREATE TABLE roles(role_id SERIAL PRIMARY KEY, role_name VARCHAR(6) UNIQUE);
CREATE TABLE users(user_id SERIAL PRIMARY KEY, first_name VARCHAR(20), last_name VARCHAR(20), email VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(20) NOT NULL, role_id INT REFERENCES roles(role_id));
CREATE TABLE countries(country_id INT PRIMARY KEY, country_name VARCHAR(50) UNIQUE NOT NULL);
CREATE TABLE vacations(vacation_id SERIAL PRIMARY KEY, country_id INT REFERENCES countries(country_id), vacation_description TEXT, beginning_date DATE, end_date DATE, price INT, picture_file_name TEXT);
CREATE TABLE likes(user_id INT REFERENCES users(user_id), vacation_id INT REFERENCES vacations(vacation_id))
