-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `whale_adoption` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `whale_adoption` DEFAULT CHARACTER SET utf8 ;
USE `whale_adoption` ;

-- -----------------------------------------------------
-- Table `whale`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `whale` ;

CREATE TABLE IF NOT EXISTS `whale` (
  `whale_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `dob` DATE NULL,
  `gender` ENUM('F', 'M') NULL,
  `mother_id` INT NULL,
  PRIMARY KEY (`whale_id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  INDEX `fk_whale_whale_idx` (`mother_id` ASC),
  CONSTRAINT `fk_whale_whale`
    FOREIGN KEY (`mother_id`)
    REFERENCES `whale` (`whale_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

truncate whale;
insert into whale values
(1, 'Flower', '2006-06-30', 'F', null),
(2, 'Finigan', '2012-07-01', 'M', 1),
(3, 'Finny', '2013-08-02', 'F', 1),
(4, 'Finster', '2018-06-10', 'M', 3),
(5, 'Fluke', '2020-08-01', null, 3),
(6, 'Fanny', null, 'F', null),
(7, 'Finky McFinkFace', '2001-08-20', 'M', 6),
(8, 'Floop', '2003-07-08', 'F', 6),
(9, 'Faerie', '2005-07-01', 'F', 8),
(10, 'Betty the Whale', '2010-07-04', 'F', 9);



-- -----------------------------------------------------
-- Table `photo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `photo` ;

CREATE TABLE IF NOT EXISTS `photo` (
  `image` BLOB NOT NULL,
  `dt` DATE NOT NULL,
  `whale_id` INT NOT NULL,
  INDEX `fk_photo_whale1_idx` (`whale_id` ASC),
  CONSTRAINT `fk_photo_whale1`
    FOREIGN KEY (`whale_id`)
    REFERENCES `whale` (`whale_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `researchteam`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `researchteam` ;

CREATE TABLE IF NOT EXISTS `researchteam` (
  `researchteam_id` INT NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `affiliation` VARCHAR(50) NOT NULL,
  `pi_lastname` VARCHAR(50) NOT NULL,
  `pi_firstname` VARCHAR(50) NOT NULL,
  `pi_email` VARCHAR(255) NOT NULL,
  `pi_phone` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`researchteam_id`))
ENGINE = InnoDB;

truncate researchteam;
insert into researchteam values
(1, 'Seal Team 6', 'New England Aquarium', 'Cousteau', 'Jacques', 'jc@neaq.org', '(617) 555-1234'),
(2, 'Jacks Whaling Project', 'Center for Coastal Studies', 'Nemo', 'Jack', 'nemo@ccs.org', '(617) 555-8888'),
(3, 'Thar be whales', 'Save the Whales', 'Scott', 'Montgomery', 'scott@stw.org', '(617) 555-0001');


-- -----------------------------------------------------
-- Table `sighting`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sighting` ;

CREATE TABLE IF NOT EXISTS `sighting` (
  `researchteam_id` INT NOT NULL,
  `whale_id` INT NOT NULL,
  `dt` DATETIME NOT NULL,
  `latitude` DOUBLE NOT NULL,
  `logitude` DOUBLE NOT NULL,
  `is_certain_ident` TINYINT NOT NULL,
  INDEX `fk_researchteamwhale_whale1_idx` (`whale_id` ASC),
  INDEX `fk_researchteamwhale_researchteam1_idx` (`researchteam_id` ASC),
  CONSTRAINT `fk_researchteamwhale_researchteam1`
    FOREIGN KEY (`researchteam_id`)
    REFERENCES `researchteam` (`researchteam_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_researchteamwhale_whale1`
    FOREIGN KEY (`whale_id`)
    REFERENCES `whale` (`whale_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

truncate sighting;
insert into sighting values
(1,1, '2021-04-05', 30.00, -65.00, True),
(1,3, '2021-04-06', 31.00, -64.00, True),
(1,4, '2021-04-07', 32.00, -65.00, False),
(1,6, '2021-04-07', 33.00, -66.00, True),
(1,9, '2021-04-07', 34.00, -67.00, False),
(2,1, '2021-04-08', 33.00, -50.00, True),
(2,3, '2021-04-09', 32.00, -60.00, True),
(2,4, '2021-04-10', 31.00, -63.00, True),
(2,4, '2021-04-11', 30.00, -65.00, True),
(2,4, '2021-04-12', 36.00, -62.00, False),
(2,9, '2021-04-12', 35.00, -63.00, False),
(2,10, '2021-04-12', 34.00, -65.00, False);


-- -----------------------------------------------------
-- Table `user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `user` ;

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` INT NOT NULL,
  `user_lastname` VARCHAR(50) NOT NULL,
  `user_firstname` VARCHAR(50) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `city` VARCHAR(50) NOT NULL,
  `state` CHAR(2) NOT NULL,
  `country` VARCHAR(50) NOT NULL,
  `zipcode` VARCHAR(10) NOT NULL,
  `telephone` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;

truncate user;
insert into user values
(1, 'Yastrzemski', 'Carl', '8 Landsdown Ave.', 'Boston', 'MA', 'USA', '02115', '(617) 555-9999'),
(2, 'Mee', 'Mary', 'Summer St.', 'Boston', 'MA', 'USA', '02115', '(617) 555-2222'),
(3, 'Williams', 'Ted', '400 Hitter Circle', 'Boston', 'MA', 'USA', '02115', '(617) 555-3333'),
(4, 'Curie', 'Marie', 'Radon St.', 'Boston', 'MA', 'USA', '02115', '(617) 555-4444'),
(5, 'Erdos', 'Paul', '10101 Discrete St.', 'Boston', 'MA', 'USA', '02115', '(617) 555-5555'),
(6, 'Codd', 'Edward Frank', '123 Relational Way', 'Cambridge', 'MA', 'USA', '02889', '(617) 555-6666');
-- -----------------------------------------------------
-- Table `creditcard`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `creditcard` ;

CREATE TABLE IF NOT EXISTS `creditcard` (
  `user_id` INT NOT NULL,
  `creditcard_num` VARCHAR(20) NOT NULL,
  `type` ENUM('AMEX', 'VISA', 'MASTERCARD', 'DISCOVER') NOT NULL,
  `expiration_month` INT NOT NULL,
  `expiration_year` INT NOT NULL,
  INDEX `fk_creditcard_user1_idx` (`user_id` ASC),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_creditcard_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

truncate creditcard;
insert into creditcard values
(1, '1234 5678 9999', 'AMEX', 6, 2024),
(3, '8888 9999 0000', 'VISA', 8, 2030),
(6, '1111 1111 1111', 'VISA', 10, 2023); 

-- -----------------------------------------------------
-- Table `adoption`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adoption` ;

CREATE TABLE IF NOT EXISTS `adoption` (
  `user_id` INT NOT NULL,
  `whale_id` INT NOT NULL,
  `dt` DATE NOT NULL,
  `auto_renew` TINYINT NOT NULL DEFAULT 1,
  `for_child` TINYINT NOT NULL,
  `charge_amt` DECIMAL(5,2) NOT NULL,
  INDEX `fk_userwhale_whale1_idx` (`whale_id` ASC),
  INDEX `fk_userwhale_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_userwhale_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_userwhale_whale1`
    FOREIGN KEY (`whale_id`)
    REFERENCES `whale` (`whale_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

truncate adoption;
insert into adoption values
(1, 5, '2021-06-24', 1, 0, 100), 
(1, 8, '2021-06-24', 1, 1, 50), 
(3, 5, '2020-09-18', 1, 1, 50),
(6, 9, '2021-10-10', 0, 0, 100);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
