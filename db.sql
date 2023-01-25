PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS students;
CREATE TABLE students (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
  name VARCHAR (32),
  courses TEXT
  );

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
  name VARCHAR (32),
  category VARCHAR (32),
  courses TEXT
  );

INSERT INTO categories (name) VALUES ('Программирование');

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
  name VARCHAR (32),
  category_id VARCHAR (32),
  FOREIGN KEY (category_id) REFERENCES category (id)
  );

INSERT INTO courses (name, category_id) VALUES ('Python', 1);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
