DROP DATABASE IF EXISTS HW3;
CREATE DATABASE HW3;
USE HW3;

CREATE TABLE Plays
(
  play_id						INT		PRIMARY KEY		AUTO_INCREMENT,
  play_title               		VARCHAR(75)		NOT NULL,
  author						VARCHAR(50)
);


CREATE TABLE Productions
(
	prod_name				VARCHAR(75)		PRIMARY KEY,
    prod_description		VARCHAR(75),
    billboard_image			BLOB,
    premiere_date			DATETIME,
    play_id					INT,
	CONSTRAINT Productions_fk_Plays
		FOREIGN KEY (play_id)
		REFERENCES Plays (play_id)
);


CREATE TABLE Actors
(
	actor_id				INT		PRIMARY KEY		AUTO_INCREMENT,
    actor_name				VARCHAR(50)		NOT NULL,
    contact_email			VARCHAR(50),
    cell_number				VARCHAR(10)
);


CREATE TABLE Characters
(
	char_id					INT		PRIMARY KEY		AUTO_INCREMENT,
    char_name				VARCHAR(50)		NOT NULL,
    char_description		VARCHAR(75),
    play_id					INT		NOT NULL,
	CONSTRAINT Characters_fk_Plays
		FOREIGN KEY (play_id)
		REFERENCES Plays (play_id)
);


CREATE TABLE Actor_Role
(
    actor_id				INT,
	prod_name				VARCHAR(50),
    char_id					INT,
	CONSTRAINT Actor_Role_fk_Actors
		FOREIGN KEY (actor_id)
		REFERENCES Actors (actor_id),
	CONSTRAINT Actor_Role_fk_Productions
		FOREIGN KEY (prod_name)
		REFERENCES Productions (prod_name),
	CONSTRAINT Actor_Role_fk_Characters
		FOREIGN KEY (char_id)
		REFERENCES Characters (char_id),
	CONSTRAINT comp_pk PRIMARY KEY (actor_id, prod_name, char_id)
);


CREATE TABLE Scenes
(
	scene_id				INT		NOT NULL,
	scene_title				VARCHAR(75)		NOT NULL,
    sequence_number			INT		NOT NULL,
	char_id				INT		NOT NULL,
	CONSTRAINT Scenes_fk_Characters
		FOREIGN KEY (char_id)
		REFERENCES Characters (char_id),
	CONSTRAINT comp_pk PRIMARY KEY (scene_id, char_id)
);


CREATE TABLE Rehearsals
(
	rehearsal_number		INT		NOT NULL,
    scene_id				INT,
    start_time				DATETIME,
	end_time				DATETIME,
	scene_duration_hours	INT,
	CONSTRAINT Rehearsals_fk_Scenes
		FOREIGN KEY (scene_id)
		REFERENCES Scenes (scene_id),
	CONSTRAINT comp_pk PRIMARY KEY (rehearsal_number, scene_id)
);


INSERT INTO Plays VALUES
(1, "Julius Caesar", NULL);

INSERT INTO Productions VALUES
("Julius Caesar the Musical", NULL, NULL, NULL, 1),
("Rosencrantz and Guildenstern are Dead", "based on the play Julius Caesar", NULL, NULL, 1);

INSERT INTO Actors VALUES
(1, "Peter O'Toole", NULL, NULL),
(2, "Will Smith", NULL, NULL),
(3, "Brad Pitt", NULL, NULL),
(4, "Russell Crowe", NULL, NULL),
(5, "Angelina Jolie", NULL, NULL),
(6, "Scarlett Johansson", NULL, NULL);

INSERT INTO Characters VALUES
(11, "Caesar", NULL, 1),
(22, "Brutus", NULL, 1),
(33, "Cassius", NULL, 1),
(44, "Antony", NULL, 1),
(55, "Portia", NULL, 1);

INSERT INTO Actor_Role VALUES
(1, "Julius Caesar the Musical", 11),
(2, "Julius Caesar the Musical", 22),
(3, "Julius Caesar the Musical", 33),
(4, "Julius Caesar the Musical", 44),
(5, "Julius Caesar the Musical", 55);

INSERT INTO Scenes VALUES
(6, "Act 3, Scene 1", 13, 11),
(6, "Act 3, Scene 1", 13, 22),
(6, "Act 3, Scene 1", 13, 33),
(6, "Act 3, Scene 1", 13, 44),
(7, "Act 3, Scene 2", 14, 22),
(7, "Act 3, Scene 2", 14, 33),
(7, "Act 3, Scene 2", 14, 44);

INSERT INTO Rehearsals VALUES
(1, 6, "2021-03-15 14:00:00", "2021-03-15 18:00:00", 2),
(1, 7, "2021-03-15 14:00:00", "2021-03-15 18:00:00", 2),
(2, 7, "2021-03-16 14:00:00", "2021-03-16 18:00:00", 4),
(3, 6, "2021-03-17 14:00:00", "2021-03-17 18:00:00", 1),
(3, 7, "2021-03-17 14:00:00", "2021-03-17 18:00:00", 3);



-- Which actors need to show up for which rehearsals?

--	SELECT DISTINCT actor_name
--	FROM Actors a
--		JOIN Actor_Role ar USING (actor_id)
--		JOIN Scenes s USING (char_id)
--		JOIN Rehearsals r USING (scene_id)
--	WHERE rehearsal_number = 1;

--	SELECT DISTINCT actor_name
--	FROM Actors a
--		JOIN Actor_Role ar USING (actor_id)
--		JOIN Scenes s USING (char_id)
--		JOIN Rehearsals r USING (scene_id)
--	WHERE rehearsal_number = 2;

--	SELECT DISTINCT actor_name
--	FROM Actors a
--		JOIN Actor_Role ar USING (actor_id)
--		JOIN Scenes s USING (char_id)
--		JOIN Rehearsals r USING (scene_id)
--	WHERE rehearsal_number = 3;

