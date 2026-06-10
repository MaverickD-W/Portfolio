DROP DATABASE IF EXISTS programming;

CREATE DATABASE programming;

USE programming;

CREATE TABLE vendors 
AS
SELECT * FROM ap.vendors;

