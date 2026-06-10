-- Load WHALE_SETUP.sql into a ROOT connection. Run the script.
-- This will generate a database called whale_adption and populate
-- the database with data.

-- Write queries for each of the questions below.
-- Take screen shots of your output for each query.  Create a PDF file
-- that consolidates your outputs for each query. 

-- Submissions using ChatGPT in whole or in part will receive a ZERO.
-- Solutions copied from other students or the internet in whole or in part will receive a ZERO
-- for all parties involved.

USE whale_adoption;
SELECT * FROM adoption;
SELECT * FROM creditcard;
SELECT * FROM photo;
SELECT * FROM researchteam;
SELECT * FROM sighting;
SELECT * FROM user;
SELECT * FROM whale;

-- 1. 
-- How much money has been collected from adoption fees?

SELECT SUM(charge_amt) AS "money_collected"
FROM adoption a;

-- 2. 
-- Count how many sightings there are for male whales and for female whales.
-- Use aliases for aggregation functions.

SELECT COUNT(s.whale_id) as "num_sightings", w.gender
FROM sighting s
	JOIN whale w USING (whale_id)
GROUP BY w.gender;

-- 3. 
-- For each adoption, list the name of the whale, the last name of the adopting user,
-- the adoption charge amount, and the type of credit card used for the adoption.

SELECT w.name, u.user_lastname, a.charge_amt, c.type
FROM whale w
	JOIN adoption a USING (whale_id)
	JOIN user u USING (user_id)
    JOIN creditcard c USING (user_id)
ORDER BY w.name DESC;

-- 4. 
-- How many total sightings were there for whales that were also adopted.
-- For example, if A was sighted 2 times, B was sighted 3 times, and C
-- was sighted 4 times, but only A and B were adopted, the query
-- should return 5.

SELECT COUNT(whale_id) as "num_adopted_sightings"
FROM adoption a
	JOIN sighting s USING (whale_id);

-- 5. 
-- The YEAR function extracts the year from a date.
-- List all users who adopted a whale in 2021.
-- Only list each user once, even if they adopted more than one whale.
-- List their first and last name and all address-related fields
-- Output the list in alphabetical order by last name.
-- The New England Aquarium plans to send these users an end-of-year holiday thank you!

SELECT DISTINCT u.user_firstname, u.user_lastname, u.address, u.city, u.state, u.country, u.zipcode
FROM user u
	JOIN adoption a ON u.user_id = a.user_id AND year(a.dt) = 2021
ORDER BY u.user_lastname;

-- 6. 
-- How much did each user spend on adoption fees?
-- Include users that didn't spend anything
-- If they didn't spend anything, show "0" rather than "null"
-- Sort users from biggest spender to smallest.
-- In case of a tie, sort by the user's last name

SELECT u.user_firstname, u.user_lastname, SUM(IFNULL(a.charge_amt, 0)) AS "total_spent"
FROM user u
	LEFT JOIN adoption a USING (user_id)
GROUP BY u.user_firstname, u.user_lastname
ORDER BY total_spent DESC, u.user_lastname;

-- 7 
-- Overall, ON AVERAGE, how many times was each whale sighted?
-- Factor into your average those whales that were never sighted.
-- I'm looking for a single number.
-- For example, if I had two whales and one was sighted 3 times and the other 0 times
-- that would be 1.5 sightings per whale.

SELECT AVG(num_sighting) AS "avg_sighting"
FROM (SELECT COUNT(s.whale_id) AS "num_sighting"
		FROM sighting s
			RIGHT JOIN whale w USING (whale_id)
		GROUP BY s.whale_id) as temp;

-- 8 
-- The MONTHNAME function takes a date and returns the name of the month (January...December).
-- The MONTH function takes a date and returns the NUMBER of month 1, 2, ..., 12.
-- How many whales were born in each month?
-- List the name of the month and the number of births.
--  You may ignore months that have no births, BUT, months should be listed in calendar order!
-- Filter out whales and counts for when the date of birth is unknown
-- Note this may not be scientifically accurate!

SELECT MONTHNAME(dob) as "birth_month", COUNT(whale_id) as "num_births"
FROM whale w
WHERE NOT dob IS NULL
GROUP BY birth_month
ORDER BY "birth_month";

-- 9 
-- For each research team, list the name and affiliation of the team,
-- The principle investigator (PI) last name,
-- The number of sightings, and the number of  sightings where the
-- identity of the whale was certain.
-- Include research teams that made no sightings
-- Zero counts should show "0" not "null"
-- Assign column aliases where appropriate
-- Sort output from most total sightings to least total sightings.

SELECT rt.name, rt.affiliation, rt.pi_lastname, COUNT(s.researchteam_id) as "num_sightings"
FROM researchteam rt
	LEFT JOIN sighting s USING (researchteam_id)
GROUP BY researchteam_id
ORDER BY num_sightings;

-- 10. 
-- What whales were sighted more than once?
-- List their names and the number of times they were sighted
-- order from most sighted to least sighted.
-- In cases of a tie, order alphabetically by the name of the whale

SELECT w.name, COUNT(s.whale_id) as "num_sighting"
FROM whale w
	JOIN sighting s USING (whale_id)
GROUP BY s.whale_id
HAVING num_sighting > 1
ORDER BY num_sighting DESC, w.name;

-- 11
-- How many times was each whale sighted and adopted?
-- Include whales that were never sighted or never adopted.
-- Make sure the total number of adoptions and sightings 
-- matches what is in the adoptions / sightings table respectively.
-- Zero adoptions or sightings should be output as "0" not null. 
-- Order your output by descending number of sightings, then descending
-- number of adoptions, then whale name.

SELECT w.name, COUNT(s.whale_id) as "num_sighting", COUNT(a.whale_id) as "num_adoption"
FROM sighting s
	RIGHT JOIN whale w USING (whale_id)
    LEFT JOIN adoption a USING (whale_id)
GROUP BY s.whale_id, a.whale_id, w.name
ORDER BY num_sighting DESC, num_adoption DESC, w.name;

-- 12. 
-- List the name and gender of every whale along with the name and gender of that whale's mother.
-- Include whales that have no known mother.
-- Add column aliases where appropriate

	SELECT w1.name, w1.gender, w2.name AS "mother_name", w2.gender AS "mother_gender"
    FROM whale w1
		LEFT JOIN whale w2 ON (w1.mother_id = w2.whale_id);

-- 13. 
-- If you examine the sighting table you will notice that 1 whale was sighted four times, 3 whales
-- were sighted twice, and two whales were sighted only once.  Four whales have not been sighted!
-- Write a query that generates these
-- statistics automatically.   We want to know how many whales were sighted k times for different
-- values of k.   You only need to include k values that apply.
-- I'm looking for a table something like this:
-- 		N	 k
-- 		1	 4
-- 		3    2
-- 		2    1
--      4    0

SELECT COUNT(num_sightings_k) AS "num_whales_n", num_sightings_k
FROM (SELECT COUNT(s.whale_id) AS "num_sightings_k"
		FROM sighting s
			RIGHT JOIN whale w USING (whale_id)
		GROUP BY w.whale_id
        ORDER BY num_sightings_k DESC) AS num_sight
GROUP BY num_sightings_k;

-- 14. 
-- Which North Atlantic Right Whales should be saved?
-- Select all the whales. Show all their attributes.
-- Don't overthink it!  ;-)

SELECT *
FROM whale w;