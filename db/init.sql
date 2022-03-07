CREATE DATABASE opencuisine;
use opencuisine;

CREATE TABLE recipes (
  title VARCHAR(20),
  total_time VARCHAR(10),
  yields VARCHAR(10),
  ingredients VARCHAR(10),
  instructions VARCHAR(10),
  image VARCHAR(10),
  host VARCHAR(10),
  links VARCHAR(10),
  nutrients VARCHAR(10)
);
CREATE TABLE users (
  id INT(11) AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  username VARCHAR(30),
  password VARCHAR(100) ,
  register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);