CREATE DATABASE opencuisine;
use opencuisine;

CREATE TABLE recipes (
  name VARCHAR(20),
  color VARCHAR(10)
);
CREATE TABLE users(
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  username VARCHAR(30),
  password VARCHAR(100),
  register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);