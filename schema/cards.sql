CREATE TABLE cards (
    card_id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,

    card_number VARCHAR(16) UNIQUE NOT NULL,
    card_type VARCHAR(10) CHECK (card_type IN ('Debit', 'Credit')),
    expiry_date DATE NOT NULL,
    cvv CHAR(3) NOT NULL,

    status VARCHAR(10) DEFAULT 'Active'
        CHECK (status IN ('Active', 'Blocked', 'Expired')),

    credit_limit NUMERIC(10,2),
    withdrawal_limit NUMERIC(10,2),

    issued_date DATE DEFAULT CURRENT_DATE,

    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
