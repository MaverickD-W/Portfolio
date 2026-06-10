-- HW5: Identifying Adverse Drug Events (ADEs) with Stored Programs
-- Prof. Rachlin
-- CS CS5200: Databases

-- We've already setup the ade database by running ade_setup.sql
-- First, make ade the active database.  Note, this database is actually based on 
-- the emr_sp schema used in the lab, but it included some extra tables.

use ade;

SELECT * FROM diagnosis;
SELECT * FROM disease;
SELECT * FROM doctor;
SELECT * FROM interaction;
SELECT * FROM medication;
SELECT * FROM patient;
SELECT * FROM prescription;
SELECT * FROM recommendation;
SELECT * FROM specialty;


-- A stored procedure to process and validate prescriptions
-- Four things we need to check
-- a) Is patient a child and is medication suitable for children?
-- b) Is patient pregnant and is medication suitable for pregnant women?
-- c) Is dosage reasonable?
-- d) Are there any adverse drug reactions


drop procedure if exists prescribe;

delimiter //
create procedure prescribe
(
	in patient_name_param varchar(255),
    in doctor_name_param varchar(255),
    in medication_name_param varchar(255),
    in ppd_param int
)
begin
	-- variable declarations (YOU MAY NOT NEED ALL OF THESE!)
    declare patient_id_var int;
    declare age_var float;
    declare is_pregnant_var boolean;
    declare weight_var int;
    declare doctor_id_var int;
    declare medication_id_var int;
    declare take_under_12_var boolean;
    declare take_if_pregnant_var boolean;
    declare mg_per_pill_var double;
    declare max_mg_per_10kg_var double;
    
	declare message varchar(255); -- The error message
    declare ddi_medication varchar(255); -- The name of a medication involved in a drug-drug interaction
    
    -- select relevant values into variables
    
-- 1 pound = about 0.45359237 kg
	SELECT (EXTRACT(YEAR FROM NOW()) - EXTRACT(YEAR FROM dob)), is_pregnant, ROUND((weight * 0.45359237),2), patient_id
    INTO age_var, is_pregnant_var, weight_var, patient_id_var
    FROM patient
    WHERE patient_name = patient_name_param;
    
    SELECT take_under_12, take_if_pregnant, mg_per_pill, max_mg_per_10kg, medication_id
	INTO take_under_12_var, take_if_pregnant_var, mg_per_pill_var, max_mg_per_10kg_var, medication_id_var
	FROM medication
	WHERE medication_name = medication_name_param;
    
    SELECT doctor_id
    INTO doctor_id_var
    FROM doctor
    WHERE doctor_name = doctor_name_param;
    
    SELECT medication_name
    INTO ddi_medication
    FROM interaction LEFT JOIN medication ON (medication_id = medication_1)
    WHERE medication_2 = medication_id_var;

    -- check age of patient and if medication ok for children
  
	
	IF age_var < 12 AND take_under_12_var = FALSE THEN
		SET message = CONCAT(medication_name_param, " cannot be prescribed to children under 12");
        SIGNAL SQLSTATE "HY000"
            SET MESSAGE_TEXT = message;
	END IF;
    
    -- check if medication ok for pregnant women
 
	
	IF is_pregnant_var = TRUE AND take_if_pregnant_var = FALSE THEN
		SET message = CONCAT(medication_name_param, " cannot be prescribed to pregnant women");
        SIGNAL SQLSTATE "HY000"
			SET MESSAGE_TEXT = message;
	END IF;
    
    -- check dosage

	
	IF ppd_param*mg_per_pill_var > (max_mg_per_10kg_var/10)*weight_var THEN
		SET message = CONCAT("Maximum dosage for ", medication_name_param, " is ", FLOOR(((max_mg_per_10kg_var/10)*weight_var)/mg_per_pill_var),
					" pills per day for patient ", patient_name_param);
        SIGNAL SQLSTATE "HY000"
			SET MESSAGE_TEXT = message;
	END IF;
    
    -- Check for reactions involving medications already prescribed to patient

    IF ddi_medication IN (SELECT medication_name
	FROM patient JOIN prescription USING (patient_id) JOIN medication USING (medication_id)
    WHERE patient_id = patient_id_var) THEN
		SET message = CONCAT(medication_name_param, " interacts with ", ddi_medication,
        " currently prescribed to ", patient_name_param);
        SIGNAL SQLSTATE "HY000"
			SET MESSAGE_TEXT = message;
    END IF;
    
    -- No exceptions thrown, so insert the prescription record
    
	INSERT INTO prescription VALUES
	(medication_id_var, patient_id_var, doctor_id_var, NOW(), ppd_param);

end //
delimiter ;


DROP TRIGGER IF EXISTS pregnant
DELIMITER //
-- Trigger for when a patient becomes pregnant
-- After you do the update, perform some checks......

CREATE TRIGGER pregnant
AFTER UPDATE ON patient
FOR EACH ROW
BEGIN

	-- Patient became pregnant

		-- Add pre-natal recommenation
        -- Delete any prescriptions that shouldn't be taken if pregnant

	IF NEW.is_pregnant = TRUE and OLD.is_pregnant = FALSE THEN
		INSERT INTO recommendation VALUES
		(patient_id, CONCAT("Take pre-natal vitamins"));
        DELETE FROM prescription
        WHERE OLD.patient_id = prescription.patient_id AND prescription.medication_id IN (SELECT DISTINCT medication_id
																							FROM medication
																							WHERE take_if_pregnant = 0);
	END IF;    
    
    -- Patient is no longer pregnant
    -- Remove pre-natal recommendation

    IF NEW.is_pregnant = FALSE and OLD.is_pregnant = TRUE THEN
		DELETE FROM recommendation
        WHERE OLD.patient_id = recommendation.patient_id
        AND recommendation.message = "Take pre-natal vitamins";
	END IF;

END //
DELIMITER ;


-- --------------------------          TEST CASES          -----------------------
-- -------------------------- DONT CHANGE BELOW THIS LINE! -----------------------
-- Test cases
truncate prescription;

-- These prescriptions should succeed
call prescribe('Jones', 'Dr.Marcus', 'Happyza', 2);
call prescribe('Johnson', 'Dr.Marcus', 'Forgeta', 1);
call prescribe('Williams', 'Dr.Marcus', 'Happyza', 1);
call prescribe('Phillips', 'Dr.McCoy', 'Forgeta', 1);

-- These prescriptions should fail
-- Pregnancy violation
call prescribe('Jones', 'Dr.Marcus', 'Forgeta', 2);

-- Age restriction
call prescribe('BillyTheKid', 'Dr.Marcus', 'Muscula', 1);

-- Excessive Dosage
call prescribe('Lee', 'Dr.Marcus', 'Foobaral', 3);

-- Drug interaction
call prescribe('Williams', 'Dr.Marcus', 'Sadza', 1);



-- Testing trigger
-- Phillips (patient_id=4) becomes pregnant
-- Verify that a recommendation for pre-natal vitamins is added
-- and that her prescription for 

update patient
set is_pregnant = True
where patient_id = 4;

select * from recommendation;
select * from prescription;


-- Phillips (patient_id=4) is no longer pregnant
-- Verify that the prenatal vitamin recommendation is gone
-- Her old prescription does not need to be added back

update patient
set is_pregnant = False
where patient_id = 4;

select * from recommendation;





