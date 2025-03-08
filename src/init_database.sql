CREATE DATABASE vacation_website_database
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
CREATE TABLE roles(role_id SERIAL PRIMARY KEY, role_name VARCHAR(6) UNIQUE);
CREATE TABLE users(user_id INT PRIMARY KEY, first_name VARCHAR(20), last_name VARCHAR(20), email VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(20) NOT NULL, role_id INT REFERENCES roles(role_id));
CREATE TABLE countries(country_id INT UNIQUE PRIMARY KEY, country_name VARCHAR(50) UNIQUE NOT NULL);
CREATE TABLE vacations(vacation_id INT UNIQUE PRIMARY KEY, country_id INT REFERENCES countries(country_id), vacation_description TEXT, beginning_date DATE, end_date DATE, price INT, picture_file_name TEXT);
CREATE TABLE likes(user_id INT REFERENCES users(user_id) ON DELETE CASCADE, vacation_id INT REFERENCES vacations(vacation_id) ON DELETE CASCADE);
INSERT INTO roles(role_name) VALUES('admin');
INSERT INTO roles(role_name) VALUES('user');
INSERT INTO users(user_id, first_name, last_name, email, password, role_id) VALUES(1, 'Asaf', 'Lotz', 'asaflotz@gmail.com',4567889,1);
INSERT INTO users(user_id, first_name, last_name, email, password, role_id) VALUES(2, 'Moti', 'Luhim', 'Motiluhim@gmail.com', 23456789, 2);
INSERT INTO countries(country_id, country_name) VALUES(1, 'Israel');
INSERT INTO countries(country_id, country_name) VALUES(2, 'Mexico');
INSERT INTO countries(country_id, country_name) VALUES(3, 'USA');
INSERT INTO countries(country_id, country_name) VALUES(4, 'France');
INSERT INTO countries(country_id, country_name) VALUES(5, 'Zanzibar');
INSERT INTO countries(country_id, country_name) VALUES(6, 'Australia');
INSERT INTO countries(country_id, country_name) VALUES(7, 'Morocco');
INSERT INTO countries(country_id, country_name) VALUES(8, 'Brazil');
INSERT INTO countries(country_id, country_name) VALUES(9, 'UK');
INSERT INTO countries(country_id, country_name) VALUES(10, 'Japan');
INSERT INTO vacations (vacation_id, country_id, vacation_description, beginning_date, end_date, price, picture_file_name) VALUES
(1, 1, 'Vacation in Tel Aviv with beautiful beaches and vibrant nightlife', '2025-09-01', '2025-09-10', 2500, 'tel_aviv.jpg'),
(2, 2, 'Vacation in Cancun with beautiful beaches and luxurious resorts', '2025-09-20', '2025-09-27', 3000, 'cancun.jpg'),
(3, 3, 'Vacation in New York with amazing cultural sites and shopping', '2025-10-05', '2025-10-12', 3500, 'new_york.jpg'),
(4, 4, 'Vacation in Paris with famous attractions like the Eiffel Tower', '2025-10-15', '2025-10-22', 4000, 'paris.jpg'),
(5, 5, 'Vacation in Zanzibar with tropical scenery and unique culture', '2025-11-01', '2025-11-10', 3200, 'zanzibar.jpg'),
(6, 6, 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800, 'sydney.jpg'),
(7, 7, 'Vacation in Marrakech with colorful markets and historical palaces', '2025-12-01', '2025-12-10', 2700, 'marrakech.jpg'),
(8, 8, 'Vacation in Rio de Janeiro with stunning beaches and grand carnival', '2025-12-15', '2025-12-25', 3100, 'rio.jpg'),
(9, 9, 'Vacation in London with famous landmarks like Big Ben and Trafalgar Square', '2025-12-26', '2026-01-02', 3300, 'london.jpg'),
(10, 10, 'Vacation in Tokyo with fascinating modern and traditional culture', '2026-01-10', '2026-01-20', 3500, 'tokyo.jpg'),
(11, 1, 'Vacation in Jerusalem with many historical and religious sites', '2026-02-01', '2026-02-10', 2800, 'jerusalem.jpg'),
(12, 6, 'Vacation in Melbourne with artistic culture and great coffee', '2026-02-15', '2026-02-22', 3600, 'melbourne.jpg');

