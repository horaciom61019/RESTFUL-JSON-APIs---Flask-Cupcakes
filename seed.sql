DROP DATABASE IF EXISTS  cupcakes_db;

CREATE DATABASE cupcakes_db;

\c cupcakes_db

CREATE TABLE cupcakes
(
  id SERIAL PRIMARY KEY,
  flavor TEXT NOT NULL,
  size TEXT NOT NULL,
  rating INT,
  image TEXT
);