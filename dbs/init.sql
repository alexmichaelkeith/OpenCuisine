CREATE DATABASE opencuisine;
use opencuisine;

CREATE USER 'myuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mypass';


GRANT USAGE ON *.* TO 'myuser'@'%' IDENTIFIED BY PASSWORD '*mypass'
GRANT USAGE ON *.* TO 'myuser'@'localhost' IDENTIFIED BY PASSWORD '*mypass'
GRANT ALL PRIVILEGES ON `opencuisine`.* TO 'myuser'@'%'
GRANT ALL PRIVILEGES ON `opencuisine`.* TO 'myuser'@'localhost'
GRANT ALL PRIVILEGES ON `opencuisine`.* TO 'myuser'@'%'
GRANT ALL PRIVILEGES ON `opencuisine`.* TO 'myuser'@'localhost'



ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';

CREATE TABLE recipes(
  name VARCHAR(20)
);

CREATE TABLE users(
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  username VARCHAR(30),
  password VARCHAR(100),
  register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);