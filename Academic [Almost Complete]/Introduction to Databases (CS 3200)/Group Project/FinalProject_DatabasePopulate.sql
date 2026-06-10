USE Newsense;

-- Reset tables before populating
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE articles_authors;
TRUNCATE TABLE articles_tags;
TRUNCATE TABLE reviews;
TRUNCATE TABLE credibility_ratings;
TRUNCATE TABLE articles;
TRUNCATE TABLE news_outlets;
TRUNCATE TABLE authors;
TRUNCATE TABLE tags;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

-- Populate news outlets
INSERT INTO news_outlets (outlet_name) VALUES ('The New York Times');
SET @nyt_id = LAST_INSERT_ID();
INSERT INTO news_outlets (outlet_name) VALUES ('The Washington Post');
SET @wash_post_id = LAST_INSERT_ID();
INSERT INTO news_outlets (outlet_name) VALUES ('WIRED Magazine');
SET @wired_id = LAST_INSERT_ID();
INSERT INTO news_outlets (outlet_name) VALUES ('The Huntington News');
SET @huntington_id = LAST_INSERT_ID();

-- Populate articles
INSERT INTO articles (news_id, article_title) VALUES (@nyt_id, 'Zohran Mamdani Elected Mayor: What This Means For NYC');
SET @nyt_article_id = LAST_INSERT_ID();
INSERT INTO articles (news_id, article_title) VALUES (@wash_post_id, 'More states are offering cheap health plans to farmers, with a catch');
SET @wash_post_article_id = LAST_INSERT_ID();
INSERT INTO articles (news_id, article_title) VALUES (@wired_id, 'Your Smart Devices Leak More Than You Think - and It''s Not Your Fault');
SET @wired_article_id_1 = LAST_INSERT_ID();
INSERT INTO articles (news_id, article_title) VALUES (@wired_id, 'Silicon Prices Are Rising. Here''s How That Impacts You');
SET @wired_article_id_2 = LAST_INSERT_ID();
INSERT INTO articles (news_id, article_title) VALUES (@huntington_id, 'What Caused the AWS Incident? A Northeastern Expert Explains');
SET @huntington_article_id_1 = LAST_INSERT_ID();
INSERT INTO articles (news_id, article_title) VALUES (@huntington_id, 'About the Northeastern Community Dogs: Cooper, Sarge, and Ryder');
SET @huntington_article_id_2 = LAST_INSERT_ID();
INSERT INTO articles (news_id, article_title) VALUES (@huntington_id, 'How Co-op''s Shape Northeastern Students'' Lives');
SET @huntington_article_id_3 = LAST_INSERT_ID();

-- Populate authors
INSERT INTO authors (author_firstname, author_lastname) VALUES ('Paws', 'Husky');
SET @paws_id = LAST_INSERT_ID();
INSERT INTO authors (author_firstname, author_lastname) VALUES ('Jimothy', 'Politics');
SET @jimothy_id = LAST_INSERT_ID();
INSERT INTO authors (author_firstname, author_lastname) VALUES ('Eliza', 'Tech');
SET @eliza_id = LAST_INSERT_ID();
INSERT INTO authors (author_firstname, author_lastname) VALUES ('Riley', 'Econ');
SET @riley_id = LAST_INSERT_ID();
INSERT INTO authors (author_firstname, author_lastname) VALUES ('Noah', 'ILoveNortheasternToAnUnhealthyDegree');
SET @noah_id = LAST_INSERT_ID();

-- Populate articles_authors join table
INSERT INTO articles_authors (article_id, author_id)
VALUES
  (@nyt_article_id, @jimothy_id),
  (@wash_post_article_id, @riley_id),
  (@wired_article_id_1, @eliza_id),
  (@wired_article_id_2, @eliza_id),
  (@huntington_article_id_1, @noah_id),
  (@huntington_article_id_2, @paws_id),
  (@huntington_article_id_3, @noah_id), -- Both Paws and Noah wrote article 3
  (@huntington_article_id_3, @paws_id);

-- Populate tags
INSERT INTO tags (tag_name) VALUES ('Politics');
SET @politics_tag_id = LAST_INSERT_ID();
INSERT INTO tags (tag_name) VALUES ('Tech');
SET @tech_tag_id = LAST_INSERT_ID();
INSERT INTO tags (tag_name) VALUES ('Econ');
SET @econ_tag_id = LAST_INSERT_ID();
INSERT INTO tags (tag_name) VALUES ('Dog');
SET @dog_tag_id = LAST_INSERT_ID();
INSERT INTO tags (tag_name) VALUES ('Northeastern');
SET @northeastern_tag_id = LAST_INSERT_ID();

-- Populate articles_tags join table
INSERT INTO articles_tags (article_id, tag_id)
VALUES
  (@nyt_article_id, @politics_tag_id),
  (@wash_post_article_id, @econ_tag_id),
  (@wash_post_article_id, @politics_tag_id),
  (@wired_article_id_1, @tech_tag_id),
  (@wired_article_id_2, @tech_tag_id),
  (@wired_article_id_2, @econ_tag_id),
  (@huntington_article_id_1, @tech_tag_id),
  (@huntington_article_id_1, @northeastern_tag_id),
  (@huntington_article_id_2, @dog_tag_id),
  (@huntington_article_id_2, @northeastern_tag_id),
  (@huntington_article_id_3, @econ_tag_id),
  (@huntington_article_id_3, @northeastern_tag_id);

-- Populate users (these hashes are just fun phrases hashed with MD5! 
-- (The real app would use something secure, like multiple rounds of bcrypt)
-- I think most of them can be found using online rainbow tables if you're curious
INSERT INTO users (username, password_hash, user_email, political_affiliation, country, region) 
  VALUES ('iokilo', '0cf6c19c14ab59d62fb99223808d6502', 'goober@example.com', 'Democrat', 'United States', 'New York');
SET @iokilo_id = LAST_INSERT_ID();
INSERT INTO users (username, password_hash, user_email, political_affiliation, country, region)
  VALUES ('jesse_blowfish', 'e26975cf2e314db045982e5d88564462', 'j.blowfish@waltuh.org', 'Libertarian', 'United States', 'Puerto Rico'); 
SET @jesse_id = LAST_INSERT_ID();
INSERT INTO users (username, password_hash, user_email, political_affiliation, country, region)
  VALUES ('general_kenobi', '161bc25962da8fed6d2f59922fb642aa', 'kenobi@starwars.com', 'Democrat', 'United States', 'New York');
SET @kenobi_id = LAST_INSERT_ID();
INSERT INTO users (username, password_hash, user_email, political_affiliation, country, region)
  VALUES ('notanevilwitch', 'e4cfb773d759bc89de1e0fe8691966be', 'witch@pinkfluffyunicorns.com', 'Republican', 'United States', 'Ohio');
SET @witch_id = LAST_INSERT_ID();

-- Populate reviews
INSERT INTO reviews (article_id, user_id, review_score, review_comment)
VALUES 
  (@nyt_article_id, @iokilo_id, 3, 'This article doesn''t cite his policies!'),
  (@wash_post_article_id, @jesse_id, 4, 'Yeah, b****, farmers!'),
  (@wired_article_id_1, @kenobi_id, 5, 'This article brilliantly explains side-channel attacks! I understand the message.'),
  (@wired_article_id_2, @witch_id, 2, 'The witch does not concern herself with technology!'),
  (@huntington_article_id_2, @witch_id, 5, 'I will be visiting Northeastern for the dogs... I need their fur for my brew! I''ll give them the BEST cute little kennel cut.');
-- The rest of these reviews don't have associated comments
INSERT INTO reviews (article_id, user_id, review_score)
VALUES 
  (@huntington_article_id_1, @iokilo_id, 4),
  (@huntington_article_id_2, @jesse_id, 5),
  (@huntington_article_id_2, @kenobi_id, 4),
  (@huntington_article_id_3, @iokilo_id, 5),
  (@huntington_article_id_3, @jesse_id, 3),
  (@huntington_article_id_3, @kenobi_id, 5),
  (@huntington_article_id_3, @witch_id, 1);

-- Populate credibility ratings
INSERT INTO credibility_ratings (rating_user_id, receiving_user_id, credibility_rating, credibility_rating_comment)
VALUES 
  (@iokilo_id, @jesse_id, 4, 'Jesse has some good points!'),
  (@iokilo_id, @kenobi_id, 3, 'Kenobi isn''t as enthusiastic about dogs as he should be...'),
  -- The witch is very misunderstood :(
  (@jesse_id, @witch_id, 2, 'Mister White taught me not to trust witches!'),
  (@kenobi_id, @witch_id, 3, 'The witch seems somewhat aligned with the force, but I''m hesitant to fully trust her yet.'),
  (@iokilo_id, @witch_id, 1, 'I hate witches!'),
  (@witch_id, @iokilo_id, 4, 'Iokilo loves dogs, so he must be a good person!'),
  (@witch_id, @jesse_id, 5, 'Jesse is a wise man!');
  
