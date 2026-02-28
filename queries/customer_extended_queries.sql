-- CUSTOMER EXTENDED QUERIES (functions 6–10)

-- (6) Transfer money (simplified outline)
-- SELECT balance FROM accounts WHERE account_id = $1 FOR UPDATE;
-- UPDATE accounts SET balance = balance - $amount WHERE account_id = $from_account;
-- UPDATE accounts SET balance = balance + $amount WHERE account_id = $to_account;
-- INSERT INTO transactions (...) VALUES (...); -- debit + credit

-- (7) Customer loans
-- SELECT * FROM loans WHERE customer_id = $1 ORDER BY created_at DESC;

-- (8) Loan EMI schedule
-- SELECT * FROM loan_emi WHERE loan_id = $1 ORDER BY emi_number ASC;

-- (9) Customer cards
-- SELECT c.*
-- FROM cards c
-- JOIN accounts a ON c.account_id = a.account_id
-- JOIN customers cu ON a.customer_id = cu.customer_id
-- WHERE cu.customer_id = $1;

-- (10) Account statement (date range)
-- SELECT * FROM transactions
-- WHERE account_id = $1
--   AND created_at::date BETWEEN $2 AND $3
-- ORDER BY created_at ASC;

