-- CS3200: Database Design
-- GAD: The Genetic Association Database

-- Write a query to answer each of the following questions
-- Save your script file as cs3200_hw2_yourname.sql (no spaces)
-- Submit this file for your homework submission

USE gad;

-- 1. 
-- Explore the content of the various columns in your gad table.
-- List all genes that are "G protein-coupled" receptors in alphabetical order by gene symbol
-- Output the gene symbol, gene name, and chromosome
-- (These genes are often the target for new drugs, so are of particular interest)

SELECT gene, gene_name, chromosome
FROM gad
WHERE gene_name LIKE "G protein-coupled%"
ORDER BY gene;

-- 2. 
-- How many records are there for each disease class?
-- Output your list from most frequent to least frequent
 
SELECT COUNT(disease_class) AS "count"
FROM gad
GROUP BY disease_class
ORDER BY count DESC;

-- 3. 
-- List all distinct phenotypes related to the disease class "IMMUNE"
-- Output your list in alphabetical order

SELECT DISTINCT phenotype
FROM gad
WHERE disease_class = "IMMUNE"
ORDER BY phenotype;

-- 4.
-- Show the immune-related phenotypes
-- based on the number of records reporting a positive association with that phenotype.
-- Display both the phenotype and the number of records with a positive association
-- Only report phenotypes with at least 60 records reporting a positive association.
-- Your list should be sorted in descending order by number of records
-- Use a column alias: "num_records"

SELECT phenotype, COUNT(association) AS "num_records"
FROM (SELECT phenotype, association
		FROM gad
		WHERE disease_class = "IMMUNE" and association = "Y") AS temp
GROUP BY phenotype
HAVING num_records >= 60
ORDER BY num_records DESC;

-- 5.
-- List the gene symbol, gene name, and chromosome attributes related
-- to genes positively linked to asthma (association = Y).
-- Include in your output any phenotype containing the substring "asthma"
-- List each distinct record once
-- Sort  gene symbol

SELECT DISTINCT gene, gene_name, chromosome
FROM gad
WHERE association = "Y" AND phenotype = "asthma"
ORDER BY gene;

-- 6. 
-- For each chromosome, over what range of nucleotides do we find
-- genes mentioned in GAD?
-- Exclude cases where the dna_start value is 0 or where the chromosome is unlisted.
-- Sort your data by chromosome. Don't be concerned that
-- the chromosome values are TEXT. (1, 10, 11, 12, ...)

SELECT MIN(dna_start) AS "min_dna_start", MAX(dna_end) AS "max_dna_end", chromosome
FROM gad
WHERE chromosome != "" AND dna_start != 0
GROUP BY chromosome
ORDER BY chromosome;

-- 7 
-- For each gene, what is the earliest and latest reported year
-- involving a positive association
-- Ignore records where the year isn't valid. (Explore the year column to determine what constitutes a valid year.)
-- Output the gene, min-year, max-year, and number of GAD records
-- order from most records to least.
-- Columns with aggregation functions should be aliased

SELECT gene, MIN(year) AS "min_year", MAX(year) AS "max_year", COUNT(association) AS "num_records"
FROM gad
WHERE association = "Y" AND year > 0
GROUP BY gene
ORDER BY num_records DESC;

-- 8. 
-- Which genes have a total of at least 100 positive association records (across all phenotypes)?
-- Give the gene symbol, gene name, and the number of associations
-- Use a 'num_records' alias in your query wherever possible

SELECT gene, gene_name, COUNT(association) AS "num_records"
FROM (SELECT gene, gene_name, association
		FROM gad
		WHERE association = "Y") AS temp2
GROUP BY gene, gene_name
HAVING num_records >= 100;

-- 9. 
-- How many total GAD records are there for each population group?
-- Sort in descending order by count
-- Show only the top five results based on number of records
-- Do NOT include cases where the population is blank

SELECT population, COUNT(population) as "num_records"
FROM gad
WHERE population != ""
GROUP BY population
ORDER BY num_records DESC
LIMIT 5;

-- 10. 
-- In question 5, we found asthma-linked genes
-- But these genes might also be implicated in other diseases
-- Output gad records involving a positive association between ANY asthma-linked gene and ANY disease/phenotype
-- Sort your output alphabetically by phenotype
-- Output the gene, gene_name, association (should always be 'Y'), phenotype, disease_class, and population
-- Hint: Use a subselect in your WHERE class and the IN operator

SELECT gene, gene_name, association, phenotype, disease_class, population
FROM gad
WHERE association = "Y" AND gene IN (
SELECT gene
FROM gad
WHERE phenotype = "asthma")
ORDER BY phenotype;

-- 11. 
-- Modify your previous query.
-- Let's count how many times each of these asthma-gene-linked phenotypes occurs
-- in our output table produced by the previous query.
-- Output just the phenotype, and a count of the number of occurrences for the top 5 phenotypes
-- with the most records involving an asthma-linked gene (EXCLUDING asthma itself).

SELECT phenotype, COUNT(phenotype) as "count"
FROM (
SELECT phenotype, gene, association
FROM gad
WHERE phenotype != "asthma") as temp3
WHERE association = "Y" AND gene IN (
SELECT gene
FROM gad
WHERE phenotype = "asthma")
GROUP BY phenotype
ORDER BY count DESC
LIMIT 5;

-- 12. 
-- Interpret your analysis

-- a) Search the Internet. Does existing biomedical research support a connection between asthma and the
-- top phenotype you identified above? Cite some sources and justify your conclusion!

-- Connection between diabetes, type 1 and asthma
-- While asthma medications tend to be cited as a contributor to diabetes, studies also find a link between type 1
-- diabetes and inflammatory diseases and the inflammatory effects of asthma.
-- However, the correlation between type 1 diabetes and asthma seems to be strongest in children with asthma,
-- as it makes them more susceptible to immune diseases. Asthma and type 1 diabetes are both commonly found in
-- children and adolescents.
-- Overall, it can be concluded that there is a link between asthma and the development of type 1 diabetes, but not as
-- much a reverse association where type 1 diabetes leads to the onset of asthma. This is because, while both do cause
-- changes in the immune system, the immune system changes - specifically the inflammatory effects - from asthma leads
-- to the possibility of further inflammatory and immune diseases.

-- b) Why might a drug company be interested in instances of such "overlapping" phenotypes?

-- It is possible that a drug company could try to develop a drug which can lessen
-- the affects of both asthma and diabetes, or the chances of becoming diabetic.
-- However, a more likely cause for interest is that asthma medications can potentially contribute to diabetes.
-- Further, steroids - used in asthma treatment - could exacerbate and possibly cause diabetes. This could lead to a
-- drug company that produces such medications facing litigations and significant revenue loss over these inadvertent effects.

-- *Sources:*
-- https://www.nature.com/articles/s41598-022-26067-4
-- https://aacijournal.biomedcentral.com/articles/10.1186/s13223-024-00869-9#:~:text=A3%20found%20that%20the%20relationship,risk%20of%20asthma%20by%2018%25.
-- https://www.medicalnewstoday.com/articles/diabetes-and-asthma
-- https://www.healthline.com/health/asthma-and-diabetes#how-theyre-related

-- CONGRATULATIONS!!: YOU JUST DID SOME LEGIT DRUG DISCOVERY RESEARCH! :-)
