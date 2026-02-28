-- CUSTOMER CORE QUERIES (functions 1–5)

-- (1) Verify customer by mobile
-- SELECT * FROM customers WHERE mobile = $1;

-- (2) Dashboard aggregates
-- SELECT COUNT(*) FROM accounts WHERE customer_id = $1;
-- SELECT SUM(balance) FROM accounts WHERE customer_id = $1;

-- (3) Customer profile
-- SELECT * FROM customers WHERE customer_id = $1;

-- (4) Transaction history
-- SELECT * FROM transactions WHERE account_id = $1 ORDER BY created_at DESC LIMIT $2;

-- (5) Customer accounts
-- SELECT * FROM accounts WHERE customer_id = $1 ORDER BY opened_at ASC;

