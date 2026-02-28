-- EMPLOYEE MANAGEMENT QUERIES (functions 11–15)

-- (11) Verify employee by ID
-- SELECT * FROM employees WHERE employee_id = $1;

-- (12) Search customers
-- SELECT * FROM customers
-- WHERE first_name ILIKE '%' || $1 || '%'
--    OR last_name  ILIKE '%' || $1 || '%'
--    OR email      ILIKE '%' || $1 || '%'
--    OR mobile     ILIKE '%' || $1 || '%';

-- (13) Get customer details (customer + accounts + loans + cards)
-- SELECT * FROM customers WHERE customer_id = $1;
-- SELECT * FROM accounts  WHERE customer_id = $1;
-- SELECT * FROM loans     WHERE customer_id = $1;
-- SELECT c.* FROM cards c
-- JOIN accounts a ON c.account_id = a.account_id
-- WHERE a.customer_id = $1;

-- (14) Create new customer
-- INSERT INTO customers (...) VALUES (...) RETURNING *;

-- (15) Create new account
-- INSERT INTO accounts (...) VALUES (...) RETURNING *;

