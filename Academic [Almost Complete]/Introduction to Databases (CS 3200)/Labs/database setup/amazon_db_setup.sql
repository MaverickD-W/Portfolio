CREATE DATABASE IF NOT EXISTS amazon_orders_db;
USE amazon_orders_db;

-- Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);

-- Orders Table

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Payment Table
CREATE TABLE payments(
	payment_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    payment_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Products Table
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    price DECIMAL(10,2)
);

-- Line items
CREATE TABLE line_items (
    order_id INT REFERENCES orders(order_id),
    order_seq INT,
    product_id INT REFERENCES products(product_id),
    constraint comp_pk PRIMARY KEY(order_id, order_seq)
);

-- Insert Sample Data
INSERT INTO customers (first_name, last_name, email) VALUES
('Alice', 'Johnson', 'alice@example.com'),
('Bob', 'Smith', 'bob@example.com'),
('Kufra', 'Anoka', 'kufra@example.com'),
('Charlie', 'Brown', 'charlie@example.com'),
('Jaden', 'Walker', 'jaden@example.com');

INSERT INTO payments (customer_id, payment_amount) VALUES
(1, 1025.00),
(1, 50.25),
(4, 200.00);


INSERT INTO orders (customer_id, order_date) VALUES
(1, '2024-02-10'),
(2, '2024-02-15'),
(4, '2024-03-01'),
(1, '2024-03-05');

INSERT INTO products (product_name, price) VALUES
('Laptop', 1000.00),
('Mouse', 25.00),
('Keyboard', 50.00),
('Monitor', 200.00);

INSERT INTO line_items (order_id, order_seq, product_id) VALUES
(1, 1, 1), -- Alice bought 1 Laptop and 1 mouse
(1, 2, 2), 
(2, 1, 3), -- Bob bought 1 Keyboard, 1 mouse, 1 monitor
(2, 2, 2), 
(2, 3, 4),
(3, 1, 4), -- Charlie bought 1 Monitor
(4, 1, 2); -- Alice bought 1 Mouse
