-- REPORTS & DB HELPERS QUERIES (functions 22–32)

-- (22) Branch report aggregates
-- SELECT COUNT(DISTINCT a.account_id) AS total_accounts,
--        COUNT(DISTINCT a.customer_id) AS total_customers,
--        COALESCE(SUM(a.balance), 0)   AS total_balance
-- FROM accounts a
-- WHERE a.branch_id = $1;

-- (23) All transactions for a branch (with filters)
-- SELECT t.*, a.account_number
-- FROM transactions t
-- JOIN accounts a ON t.account_id = a.account_id
-- WHERE a.branch_id = $1;

-- (24) Get account by ID
-- SELECT * FROM accounts WHERE account_id = $1;

-- (25) Get account balance
-- SELECT balance FROM accounts WHERE account_id = $1;

-- (26) Update account balance
-- UPDATE accounts SET balance = $2 WHERE account_id = $1;

-- (27) Create transaction (with balance update)
-- see customer_extended / db_helpers implementation.

-- (28) Get loan by ID
-- SELECT * FROM loans WHERE loan_id = $1;

-- (29) Get branch by ID
-- SELECT * FROM branches WHERE branch_id = $1;

-- (30) Get employee by ID
-- SELECT * FROM employees WHERE employee_id = $1;

-- (31) Validate account exists by number
-- SELECT 1 FROM accounts WHERE account_number = $1;

-- (32) Check sufficient balance
-- SELECT balance >= $2 AS ok FROM accounts WHERE account_id = $1;

