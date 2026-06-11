USE amazon_orders_db;

-- 1. List all unique customers who have placed orders. Include first and last name.
-- a) do with implicit syntax
-- b) do with explicit syntat

-- a)
SELECT DISTINCT first_name, last_name
FROM customers c, orders o
WHERE c.customer_id = o.customer_id;

-- b) 
SELECT DISTINCT first_name, last_name
FROM customers c JOIN orders o
	ON c.customer_id = o.customer_id;
    
-- 2. Find what products where bought by which user. Exclude users who made no orders.
-- If a user made more than one order there should be more than one row for them.

SELECT product_name, first_name, last_name
FROM products p
	JOIN line_items li
		ON p.product_id = li.product_id
	JOIN orders o
		ON li.order_id = o.order_id
	JOIN customers c
		ON o.customer_id = c.customer_id;
    
-- 3. Find all payments Alice Johnson made
-- Print out the payment amount. If there was more than one payment, it's ok for it
-- to be in different rows, we want each "transaction"

SELECT payment_amount
FROM payments p JOIN customers c
	ON p.customer_id = c.customer_id
WHERE first_name = "Alice" AND last_name = "Johnson";

