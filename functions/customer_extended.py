"""
Extended customer operations (functions 6–10).

Includes money transfers, loans, cards, and account statements.
"""

from __future__ import annotations

import csv
import os
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from db import get_cursor, fetch_all, fetch_one
from . import db_helpers


def transfer_money(
    from_account: int,
    to_account: int,
    amount: float,
    description: str = "Transfer",
) -> Tuple[bool, str]:
    """
    (6) Transfer money between two accounts.

    Performs basic validations and a single DB transaction that:
    - locks both accounts
    - checks sufficient balance
    - updates balances
    - inserts two transaction rows (debit and credit)
    """
    if from_account == to_account:
        return False, "Source and destination accounts must be different."

    amt = Decimal(str(amount))
    if amt <= 0:
        return False, "Amount must be positive."

    if not db_helpers.check_sufficient_balance(from_account, amt):
        return False, "Insufficient balance."

    with get_cursor(commit=True) as cur:
        # Lock both accounts in a deterministic order to avoid deadlocks
        acc_ids = sorted([from_account, to_account])
        cur.execute(
            """
            SELECT account_id, balance
            FROM accounts
            WHERE account_id = ANY(%s)
            FOR UPDATE
            """,
            (acc_ids,),
        )
        rows = {row["account_id"]: row for row in cur.fetchall()}

        if from_account not in rows or to_account not in rows:
            raise ValueError("One or both accounts not found.")

        from_balance = rows[from_account]["balance"]
        to_balance = rows[to_account]["balance"]

        if from_balance < amt:
            return False, "Insufficient balance."

        new_from_balance = from_balance - amt
        new_to_balance = to_balance + amt

        # Update balances
        cur.execute(
            "UPDATE accounts SET balance = %s WHERE account_id = %s",
            (new_from_balance, from_account),
        )
        cur.execute(
            "UPDATE accounts SET balance = %s WHERE account_id = %s",
            (new_to_balance, to_account),
        )

        # Insert transactions
        cur.execute(
            """
            INSERT INTO transactions (
                account_id, tx_type, amount, balance_after, related_account, description
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (from_account, "DEBIT", amt, new_from_balance, to_account, description),
        )
        cur.execute(
            """
            INSERT INTO transactions (
                account_id, tx_type, amount, balance_after, related_account, description
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (to_account, "CREDIT", amt, new_to_balance, from_account, description),
        )

    return True, "Transfer completed successfully."


def get_customer_loans(customer_id: int) -> List[Dict[str, Any]]:
    """
    (7) Fetch all loans belonging to a customer.
    """
    return fetch_all(
        """
        SELECT
            l.*,
            a.account_number,
            b.branch_name
        FROM loans l
        JOIN accounts a ON l.linked_account_id = a.account_id
        JOIN branches b ON l.branch_id = b.branch_id
        WHERE l.customer_id = %s
        ORDER BY l.created_at DESC
        """,
        (customer_id,),
    )


def get_loan_emi_schedule(loan_id: int) -> List[Dict[str, Any]]:
    """
    (8) Get EMI schedule rows for a given loan.
    """
    return fetch_all(
        """
        SELECT *
        FROM loan_emi
        WHERE loan_id = %s
        ORDER BY emi_number ASC
        """,
        (loan_id,),
    )


def get_customer_cards(customer_id: int) -> List[Dict[str, Any]]:
    """
    (9) Fetch all cards linked to a customer's accounts.
    """
    return fetch_all(
        """
        SELECT
            c.*,
            a.account_number,
            a.account_type
        FROM cards c
        JOIN accounts a ON c.account_id = a.account_id
        JOIN customers cu ON a.customer_id = cu.customer_id
        WHERE cu.customer_id = %s
        ORDER BY c.issued_date DESC
        """,
        (customer_id,),
    )


def _calculate_emi(principal: Decimal, annual_rate: float, tenure_months: int) -> Decimal:
    """Simple EMI calculation helper."""
    if tenure_months <= 0:
        return Decimal("0.00")

    monthly_rate = Decimal(str(annual_rate)) / Decimal("1200")
    if monthly_rate == 0:
        return (principal / tenure_months).quantize(Decimal("0.01"))

    # Use float math for simplicity, then convert back to Decimal
    p = float(principal)
    r = float(monthly_rate)
    n = tenure_months
    emi = p * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return Decimal(str(round(emi, 2)))


def request_loan(
    customer_id: int,
    account_id: int,
    loan_type: str,
    principal_amount: float,
    tenure_months: int,
) -> Tuple[bool, str]:
    """
    Create a new PENDING loan request for the customer.
    """
    # Validate account belongs to this customer
    account = fetch_one(
        "SELECT account_id, customer_id, branch_id FROM accounts WHERE account_id = %s",
        (account_id,),
    )
    if not account or account["customer_id"] != customer_id:
        return False, "Invalid account selected."

    if principal_amount <= 0 or tenure_months <= 0:
        return False, "Amount and tenure must be positive."

    principal = Decimal(str(principal_amount))

    # Basic interest-rate defaults by loan type
    rate_by_type = {
        "Personal": 12.0,
        "Home": 8.5,
        "Auto": 9.0,
        "Education": 9.0,
        "Business": 11.0,
    }
    interest_rate = rate_by_type.get(loan_type, 10.0)
    emi_amount = _calculate_emi(principal, interest_rate, tenure_months)

    # Generate a simple unique-ish loan_number based on next ID
    next_row = fetch_one("SELECT COALESCE(MAX(loan_id), 0) + 1 AS next_id FROM loans")
    next_id = next_row["next_id"]
    loan_number = f"LN{int(next_id):010d}"

    row = fetch_one(
        """
        INSERT INTO loans (
            customer_id,
            branch_id,
            linked_account_id,
            loan_number,
            loan_type,
            principal_amount,
            interest_rate,
            tenure_months,
            emi_amount,
            outstanding_balance,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'PENDING')
        RETURNING *
        """,
        (
            customer_id,
            account["branch_id"],
            account_id,
            loan_number,
            loan_type,
            principal,
            interest_rate,
            tenure_months,
            emi_amount,
            principal,
        ),
    )

    if not row:
        return False, "Could not create loan request."

    return True, "Loan request submitted successfully."

def generate_account_statement(
    account_id: int,
    start_date: Optional[date],
    end_date: Optional[date],
    export_to_csv: bool = False,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    (10) Generate an account statement (optionally as CSV).

    Returns (rows, csv_path). If `export_to_csv` is False, csv_path is None.
    """
    params: list[Any] = [account_id]
    where = ["t.account_id = %s"]

    if start_date:
        where.append("t.created_at::date >= %s")
        params.append(start_date)
    if end_date:
        where.append("t.created_at::date <= %s")
        params.append(end_date)

    sql = f"""
        SELECT
            t.tx_id,
            t.created_at,
            t.tx_type,
            t.amount,
            t.balance_after,
            t.related_account,
            t.description
        FROM transactions t
        WHERE {" AND ".join(where)}
        ORDER BY t.created_at ASC, t.tx_id ASC
    """

    rows = fetch_all(sql, tuple(params))

    csv_path: Optional[str] = None
    if export_to_csv:
        os.makedirs("statements", exist_ok=True)
        filename = f"statement_account_{account_id}.csv"
        csv_path = os.path.join("statements", filename)

        with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Tx ID", "Date", "Type", "Amount", "Balance After", "Related Account", "Description"]
            )
            for r in rows:
                writer.writerow(
                    [
                        r["tx_id"],
                        r["created_at"],
                        r["tx_type"],
                        r["amount"],
                        r["balance_after"],
                        r["related_account"],
                        r["description"],
                    ]
                )

    return rows, csv_path

