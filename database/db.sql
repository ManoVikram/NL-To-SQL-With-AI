CREATE DATABASE learningAI;

CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  signup_date DATE,
  total_spent DECIMAL(10, 2)
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id),
  order_date TIMESTAMP,
  total_amount DECIMAL(10, 2),
  status VARCHAR(20)
);

INSERT INTO customers (name, email, signup_date, total_spent) VALUES
  ('Alice Johnson', 'alice@example.com', '2024-01-15', 1250.00),
  ('Bob Smith', 'bob@example.com', '2024-02-20', 890.50),
  ('Carol White', 'carol@example.com', '2024-03-10', 2100.75),
  ('David Johnson', 'david@example.com', '2025-10-10', 1234.12),
  ('Ethan Rhodes', 'ethan@example.com', '2025-01-01', 123.12),
  ('Featherington', 'featherington@example.com', '2023-12-02', 2345.86),
  ('Grace Miller', 'grace.m@example.com', '2024-05-12', 450.25),
  ('Henry Vance', 'henry.vance@example.com', '2024-08-30', 3105.00),
  ('Isla Fischer', 'isla.f@example.com', '2025-02-14', 85.50),
  ('Jack Dawson', 'jack.d@example.com', '2025-06-22', 1520.40);

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
  (1, '2024-06-10 10:30:00', 450.00, 'completed'),
  (1, '2024-07-15 14:20:00', 800.00, 'completed'),
  (2, '2024-02-21 09:15:00', 500.00, 'completed'),
  (2, '2024-03-05 16:45:00', 390.50, 'completed'),
  (3, '2024-03-12 11:00:00', 1200.75, 'completed'),
  (3, '2024-04-20 13:10:00', 900.00, 'shipped'),
  (4, '2025-10-12 08:30:00', 1234.12, 'processing'),
  (5, '2025-01-05 10:20:00', 123.12, 'completed'),
  (6, '2023-12-05 14:00:00', 2000.00, 'completed'),
  (6, '2024-01-10 09:45:00', 345.86, 'completed'),
  (7, '2024-05-15 12:00:00', 450.25, 'shipped'),
  (8, '2024-09-01 15:30:00', 3105.00, 'completed');