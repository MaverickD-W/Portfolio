DROP DATABASE IF EXISTS Newsense;
CREATE DATABASE Newsense;
USE Newsense;

CREATE TABLE news_outlets (
  news_id INT PRIMARY KEY AUTO_INCREMENT,
  outlet_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE authors ( 
  author_id INT PRIMARY KEY AUTO_INCREMENT,
  author_firstname VARCHAR(50) NOT NULL,
  author_lastname VARCHAR(50) NOT NULL
);

CREATE TABLE articles (
  article_id INT PRIMARY KEY AUTO_INCREMENT,
  news_id INT NOT NULL, -- News outlet source
  article_title VARCHAR(255) NOT NULL, 
  CONSTRAINT fk_outlets_articles 
    FOREIGN KEY (news_id) 
    REFERENCES news_outlets (news_id)
);

CREATE TABLE articles_authors ( -- Many-to-Many join table for articles and authors
  article_id INT NOT NULL,
  author_id INT NOT NULL,
  CONSTRAINT pk_articles_authors 
    PRIMARY KEY (article_id, author_id),
  CONSTRAINT fk_articles_authors_articles 
    FOREIGN KEY (article_id) 
    REFERENCES articles (article_id),
  CONSTRAINT fk_articles_authors_authors
    FOREIGN KEY (author_id) 
    REFERENCES authors (author_id)
);

CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE, 
  password_hash VARCHAR(60) NOT NULL, -- Bcrypt hash size
  user_email VARCHAR(255) NOT NULL UNIQUE, -- Max email address length is 254 characters
  -- Below are all optional inputs that a user can put in their profile
  political_affiliation VARCHAR(50), 
  country VARCHAR(50),
  region VARCHAR(50) -- This would include states, provinces, etc.
);

CREATE TABLE tags ( -- Articles can have tags to categorize them
  tag_id INT PRIMARY KEY AUTO_INCREMENT,
  tag_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE articles_tags ( -- Many-to-Many join table for articles and tags
  article_id INT NOT NULL,
  tag_id INT NOT NULL,
  CONSTRAINT pk_articles_tags 
    PRIMARY KEY (article_id, tag_id),
  CONSTRAINT fk_articles_tags_articles 
    FOREIGN KEY (article_id) 
    REFERENCES articles (article_id),
  CONSTRAINT fk_articles_tags_tags
    FOREIGN KEY (tag_id) 
    REFERENCES tags (tag_id)
);

CREATE TABLE reviews ( -- Users can review articles
  article_id INT NOT NULL,
  user_id INT NOT NULL,
  review_score TINYINT NOT NULL, 
  review_comment VARCHAR(500), -- Constrain max review length to 500 characters
  CONSTRAINT pk_reviews 
    PRIMARY KEY (article_id, user_id),
  CONSTRAINT fk_articles_reviews 
    FOREIGN KEY (article_id) 
    REFERENCES articles (article_id),
  CONSTRAINT fk_users_reviews 
    FOREIGN KEY (user_id) 
    REFERENCES users (user_id)
);

CREATE TABLE credibility_ratings ( -- Users can rate other users on their profiles
  rating_user_id INT NOT NULL,
  receiving_user_id INT NOT NULL,
  credibility_rating TINYINT NOT NULL, 
  credibility_rating_comment VARCHAR(500), -- Constraint max review length to 500 characters
  CONSTRAINT pk_ratings 
    PRIMARY KEY (rating_user_id, receiving_user_id),
  CONSTRAINT fk_users_ratings_1 
    FOREIGN KEY (rating_user_id) 
    REFERENCES users (user_id),
  CONSTRAINT fk_users_ratings_2 
    FOREIGN KEY (receiving_user_id) 
    REFERENCES users (user_id)
);
