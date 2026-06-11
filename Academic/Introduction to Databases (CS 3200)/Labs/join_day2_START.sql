USE amazon_orders_db;

-- 1. Determine all payments customers have made. Include all customers in your output.
-- You should be listing customer first name, last name, and payment amount.
-- If a customer has made more than one payment, it's ok to have it in a different row.

SELECT c.first_name, c.last_name, pa.payment_amount
FROM customers c
LEFT JOIN payments pa USING (customer_id);


-- 2. How many mice were ordered?
-- Hint 1: Use a derived table
-- Hint 2: In your derived table you only need to use two different tables
-- Hint 3: You will need a subquery to determine which product id a mouse is

SELECT COUNT(product_id) as "num_mouse"
FROM products pr
JOIN line_items li USING (product_id)
WHERE pr.product_name = "Mouse";


-- 3. What customers never placed an order?

SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
LEFT JOIN orders o USING (customer_id)
WHERE order_id IS NULL;
