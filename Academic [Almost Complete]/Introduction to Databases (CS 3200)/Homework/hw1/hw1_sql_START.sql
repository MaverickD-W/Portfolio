 
# CS 3200: Database Systems
# Prof. Ithier
# Homework 1 (Part C)
# Using the Murach sample databases, 
# write a query or multiple queries to answer the questions below
# Output only the attributes needed to answer the question
# Do NOT use JOINS, SUBQUERIES or other advanced SQL techniques

USE ap;

# Hint: look at the table names and their columns that are available in the ap database before beginning

-- 1. What vendors are in Massachusetts?

SELECT vendor_name
FROM vendors
WHERE vendor_state = "MA";

-- 2. In what states can I find vendors?
-- List each state once

SELECT DISTINCT vendor_state
FROM vendors;

-- 3. How many vendors are based in either Wisconsin or California?

SELECT COUNT(vendor_state) AS "count"
FROM vendors
WHERE vendor_state IN ("WI", "CA");

-- 4. What vendors have a name containing the phrase "Inc or Inc."

SELECT vendor_name
FROM vendors
WHERE vendor_name LIKE "%Inc%";

-- 5. Report the invoice number, invoice date, and credit total for any invoices
-- whose credit total is at least $1000 and less than or equal to $5000.

SELECT invoice_number, invoice_date, credit_total
FROM invoices
WHERE credit_total >= 1000 AND credit_total <= 5000;

-- Switch to ex database
USE ex;

-- Hint, like before, explore which tables and what columns they have in this db that might help you

-- 6. What employees report directly to Elmer Jones?
-- List all the attributes of the employee. You are allowed to use multiple queries and hardcode.
-- We'll learn a better way to do this later

SELECT last_name, first_name, employee_id
FROM employees
WHERE last_name = "Jones" AND first_name = "Elmer";
-- Elemer Jones' employee_id is 2, - as provided by the above query - and will be used in the query below.
SELECT *
FROM employees
WHERE manager_id = 2;


-- 7. What is the NAME of the department of the employees who are working on project P1012?
-- Return only the department name.  Show all queries leading to your answer.

SELECT project_number, employee_id
FROM projects
WHERE project_number = "P1012";
-- employee ids from project P1012 are 1,3,5
SELECT employee_id, department_number
FROM employees
WHERE employee_id IN (1,3,5);
-- department_number from employee ids 1,3,5 is 2
SELECT department_name
FROM departments
WHERE department_number = 2;

-- 8. What project or projects are people in the Personnel department working on?
-- Show all queries contributing to your investigation.

SELECT department_name, department_number
FROM departments
WHERE department_name = "Personnel";
-- department_number from department_name Personnel is 4
SELECT department_number, employee_id
FROM employees
WHERE department_number = 4;
-- employee ids from department_number 4 are 2,8
SELECT project_number
FROM projects
WHERE employee_id IN (2,8);

