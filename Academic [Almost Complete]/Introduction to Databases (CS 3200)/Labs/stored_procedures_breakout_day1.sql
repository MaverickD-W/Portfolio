USE emr_sp;

SHOW TABLES;

SELECT * FROM diagnosis;
SELECT * FROM disease;
SELECT * FROM doctor;
SELECT * FROM patient;
SELECT * FROM recommendation;
SELECT * FROM specialty;

-- create a procedure called "doctor_num_diagnoses" that when
-- given a dr name, it finds number of diagnoses they made
-- if they made 1+ diagnoses, output a message saying how many 
-- (ex "Dr.X made 8 diagnoses!")
-- if no diagnosis say "Dr.X made no diagnoses!"
-- (replace X, with doctor name)


-- drop procedure if it already exists
DROP PROCEDURE IF EXISTS doctor_num_diagnoses;
-- change delimiter
DELIMITER //
-- create procedure with logic
CREATE PROCEDURE doctor_num_diagnoses(IN doctor_name_param VARCHAR(50))
BEGIN
	DECLARE num_diagnosis_var INT DEFAULT 0;
    SELECT COUNT(disease_id) AS "num_diagnosis"
    INTO num_diagnosis_var
	FROM doctor d LEFT JOIN diagnosis p USING (doctor_id)
    WHERE d.doctor_name = doctor_name_param;
    
    IF num_diagnosis_var = 0 THEN
	SELECT CONCAT("Dr. ", doctor_name_param, "made no diagnoses") AS MESSAGE;
	ELSEIF num_diagnosis_var >= 1 THEN
	SELECT CONCAT("Dr. ", doctor_name_param, "made ", num_diagnosis_var, " diagnoses") AS MESSAGE;
    END IF;

END //
    
-- change delimiter
DELIMITER ;

CALL doctor_num_diagnoses("Quinn");
CALL doctor_num_diagnoses("Oz");
CALL doctor_num_diagnoses("House");
