DROP DATABASE IF EXISTS emr_sp;
CREATE DATABASE  IF NOT EXISTS emr_sp;
USE emr_sp;


-- DISEASE

DROP TABLE IF EXISTS disease;
CREATE TABLE disease (
  disease_id INT PRIMARY KEY,
  disease_name VARCHAR(100) DEFAULT NULL
) ;

INSERT INTO disease VALUES 
(1,'Cold'),
(2,'Flu'),
(3,'Typhus'), 
(4, 'The plague'), 
(5, 'Flesh-eating bacteria');


-- SPECIALTY
DROP TABLE IF EXISTS  specialty;
CREATE TABLE specialty (
	specialty_id INT PRIMARY KEY AUTO_INCREMENT,
    specialty_name VARCHAR(20)
);

INSERT INTO specialty (specialty_name) VALUES
('GENERAL PRACTITIONER'),
('CARDIOLOGY'),
('UROLOGY'),
('DIAGNOSTICS'),
('BRAIN SURGERY'),
('INTERNAL MEDICINE');



-- DOCTOR

DROP TABLE IF EXISTS doctor;
CREATE TABLE doctor (
  doctor_id INT PRIMARY KEY,
  doctor_name VARCHAR(100) DEFAULT NULL,
  specialty_id INT NULL,
  CONSTRAINT fk_doctor_spec FOREIGN KEY (specialty_id) REFERENCES specialty (specialty_id)
) ;

INSERT INTO doctor VALUES 
(1,'Marcus', 5),
(2,'House', 4),
(3,'Howser', 1),
(4,'Quinn', 1),
 (5, 'Oz', 2),
 (6, 'McCoy', null),
 (7, 'Cooper', 1),
 (8, 'Crusher', 4);

-- PATIENT

DROP TABLE IF EXISTS patient;
CREATE TABLE patient (
  patient_id INT PRIMARY KEY,
  patient_name VARCHAR(100) DEFAULT NULL,
  sex CHAR(1) DEFAULT NULL,
  is_pregnant BOOLEAN DEFAULT FALSE,
  flushot BOOLEAN DEFAULT NULL,
  state CHAR(2) DEFAULT NULL,
  dob DATE DEFAULT NULL,
  height FLOAT DEFAULT NULL,
  weight FLOAT DEFAULT NULL,
  pcp_id INT NOT NULL,
  
  CONSTRAINT fk_patient_pcp FOREIGN KEY (pcp_id) REFERENCES doctor (doctor_id)

);


INSERT INTO patient VALUES 
(1,'Smith','M',0,1,'VT','1995-01-22',72,240,3),
(2,'Jones','F',1,0,'MA','1964-12-29',71.5,160,3),
(3,'Johnson','F', 0,1,'MA','1922-04-22',65,130,3),
(4,'Phillips','F',0,1,'MA','1999-11-11',61,116,3),
(5,'Lee','M', 0, 0,'CT','1970-10-08',73,240,3),
(6,'Marcus','M', 0, 0,'NY','1966-02-01',70,150,4),
(7,'Samuels','F', 0, 0,'CA','1969-08-11',68,130,4),
(8,'van Dyke','M', 0, 0,'CA','1978-03-27',71,165,4);


-- DIAGNOSIS

DROP TABLE IF EXISTS diagnosis;
CREATE TABLE diagnosis (
  doctor_id INT NOT NULL,
  patient_id INT NOT NULL,
  disease_id INT NOT NULL,
  diagnosis_date date DEFAULT NULL,
  CONSTRAINT fk_diag_doc FOREIGN KEY (doctor_id) REFERENCES doctor (doctor_id),
  CONSTRAINT fk_diag_pat  FOREIGN KEY (patient_id) REFERENCES patient (patient_id),
  CONSTRAINT fk_diag_dis FOREIGN KEY (disease_id) REFERENCES disease (disease_id)
) ;

INSERT INTO diagnosis VALUES 
(1,1,1, '2016-01-11'),
(1,1,3, '2016-11-22'),
(3,1,1, '2017-05-15'),
(1,2,2, '2017-03-19'),
(3,2,2, '2016-02-23'),
(1,2,1, '2016-06-04'),
(2,3,1, '2016-09-12'),
(2,3,2, '2017-04-15'),
(2,4,1, '2016-03-30'),
(4,4,3, '2016-08-31'),
(2,5,2, '2016-01-08'),
(2,6,2, '2017-11-01'),
(3,7,2, '2016-06-19');



-- RECOMMENDATIONS

DROP TABLE IF EXISTS recommendation;
CREATE TABLE recommendation (
  patient_id INT NOT NULL,
  message VARCHAR(255) NOT NULL,
  CONSTRAINT fk_recommendations FOREIGN KEY (patient_id) REFERENCES patient (patient_id)
) ;




