CREATE DATABASE breakout;
USE breakout;

CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    major VARCHAR(50),
    year INT,
    gpa DECIMAL(3,2)
);

INSERT INTO students (id, name, major, year, gpa) VALUES
(1, 'Kufre Smith', 'Computer Sci', 2, 3.8),
(2, 'Xi Johnson', 'Math', 1, 3.1),
(3, 'Cara Patel', 'Biology', 3, 3.5),
(4, 'David Kim', 'Math', 4, 3.9),
(5, 'Emily Zhang', 'History', 2, 3.0),
(6, 'Tyrone White', 'Computer Sci', 1, 2.8),
(7, 'Grace Liu', 'Math', 3, 3.6);

