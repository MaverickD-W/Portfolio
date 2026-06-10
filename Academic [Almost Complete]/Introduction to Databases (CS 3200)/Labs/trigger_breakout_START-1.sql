USE emr_sp;

SELECT * FROM diagnosis;
SELECT * FROM disease;
SELECT * FROM doctor;
SELECT * FROM patient;
SELECT * FROM recommendation;
SELECT * FROM specialty;

-- Create a trigger called "dr_check_in" that makes a recommendation 
-- to a patient to "Please follow up with provider X about your Y diagnosis"
-- any time they get a new diagnosis
-- X and Y should replaced with doctor name and diagnosis name, respectively

-- drop the trigger if needed
DROP TRIGGER IF EXISTS dr_check_in;

-- set delimiter
DELIMITER //

-- create trigger
CREATE TRIGGER dr_check_in
	-- trigger body
AFTER UPDATE ON diagnosis
	FOR EACH ROW
BEGIN
	SELECT COUNT(disease_id) as "num_diag"
    FROM (SELECT *
		FROM doctor doc,
			RIGHT JOIN diagnosis diag USING (doctor_id)
			LEFT JOIN disease dis USING (disease_id)) AS combined
		GROUP BY patient_id;
	IF OLD.num_diag > NEW.num_diag THEN
		INSERT INTO recommendation VALUES
        (NEW.patient_id, "Please follow up with provider ", , " about your ", , " diagnosis");
	END IF;

END //
-- change delimiter back
 

-- Test your trigger works
SELECT * FROM recommendation;

INSERT INTO diagnosis VALUES (4, 5, 1, '2016-03-02');

SELECT * FROM recommendation; -- this should show the new recommendation