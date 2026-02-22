SELECT employee_id, name, role, salary, status 
FROM employees 
ORDER BY employee_id;


INSERT INTO cards 
(account_id, card_number, card_type, expiry_date, cvv, status, credit_limit, withdrawal_limit)
VALUES
-- Rahul Sharma (account 1)
(1, '4532123412341111', 'Debit',  '2029-12-31', '123', 'Active', NULL, 20000),
(1, '4532123412341112', 'Credit', '2031-06-30', '321', 'Active', 50000, NULL),

-- Priya Mehta (account 2)
(2, '4532123412342221', 'Debit',  '2029-03-31', '234', 'Active', NULL, 18000),
(2, '4532123412342222', 'Credit', '2030-11-30', '432', 'Active', 100000, NULL),

-- Arjun Nair (account 3)
(3, '4532123412343331', 'Debit',  '2028-10-31', '345', 'Active', NULL, 15000),

-- Sneha Reddy (account 4)
(4, '4532123412344441', 'Debit',  '2029-09-30', '456', 'Active', NULL, 25000),
(4, '4532123412344442', 'Credit', '2032-02-28', '654', 'Active', 75000, NULL),

-- Vikram Singh (account 5)
(5, '4532123412345551', 'Debit',  '2029-05-31', '567', 'Active', NULL, 12000),
(5, '4532123412345552', 'Credit', '2031-08-31', '765', 'Active', 60000, NULL);
