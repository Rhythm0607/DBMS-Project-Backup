-- EMPLOYEE LOANS & CARDS QUERIES (functions 16–21)

-- (16) Pending loans for a branch
-- SELECT * FROM loans WHERE branch_id = $1 AND status = 'PENDING';

-- (17) All loans for a branch (optional status)
-- SELECT * FROM loans WHERE branch_id = $1 AND status = COALESCE($2, status);

-- (18) Approve loan
-- UPDATE loans
-- SET status = 'APPROVED', employee_id = $2, disbursement_date = CURRENT_DATE
-- WHERE loan_id = $1;

-- (19) Reject loan
-- UPDATE loans
-- SET status = 'REJECTED', employee_id = $2
-- WHERE loan_id = $1;

-- (20) Issue new card
-- INSERT INTO cards (...) VALUES (...) RETURNING *;

-- (21) All cards in a branch
-- SELECT c.*
-- FROM cards c
-- JOIN accounts a ON c.account_id = a.account_id
-- WHERE a.branch_id = $1;

