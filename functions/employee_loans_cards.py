"""
Employee loan and card management (functions 16–21).
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional
import random

from db import fetch_one, fetch_all, execute, get_cursor


def get_pending_loans(branch_id: int) -> List[Dict[str, Any]]:
    """
    (16) Get all pending loans for a branch.
    """
    return fetch_all(
        """
        SELECT
            l.*,
            c.first_name,
            c.last_name,
            a.account_number
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        JOIN accounts a ON l.linked_account_id = a.account_id
        WHERE l.branch_id = %s AND l.status = 'PENDING'
        ORDER BY l.created_at ASC
        """,
        (branch_id,),
    )


def get_all_loans(branch_id: int, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    (17) Get all loans for a branch, optionally filtered by status.
    """
    params: list[Any] = [branch_id]
    where = ["l.branch_id = %s"]

    if status_filter:
        where.append("l.status = %s")
        params.append(status_filter)

    sql = f"""
        SELECT
            l.*,
            c.first_name,
            c.last_name,
            a.account_number
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        JOIN accounts a ON l.linked_account_id = a.account_id
        WHERE {" AND ".join(where)}
        ORDER BY l.created_at DESC
    """

    return fetch_all(sql, tuple(params))


def approve_loan(loan_id: int, employee_id: int) -> None:
    """
    (18) Mark a loan as approved and associate approving employee.
    """
    execute(
        """
        UPDATE loans
        SET status = 'APPROVED',
            employee_id = %s,
            disbursement_date = CURRENT_DATE
        WHERE loan_id = %s
        """,
        (employee_id, loan_id),
    )


def reject_loan(loan_id: int, employee_id: int) -> None:
    """
    (19) Reject a loan.
    """
    execute(
        """
        UPDATE loans
        SET status = 'REJECTED',
            employee_id = %s
        WHERE loan_id = %s
        """,
        (employee_id, loan_id),
    )


def _generate_card_number() -> str:
    """Generate a pseudo-random 16-digit card number."""
    return "".join(str(random.randint(0, 9)) for _ in range(16))


def _generate_cvv() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(3))


def issue_new_card(
    account_id: int,
    card_type: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    (20) Issue a new card for an account.
    """
    card_number = _generate_card_number()
    cvv = _generate_cvv()

    # Default expiry: 4 years from today
    expiry = date.today().replace(year=date.today().year + 4)

    credit_limit = data.get("credit_limit")
    withdrawal_limit = data.get("withdrawal_limit")

    row = fetch_one(
        """
        INSERT INTO cards (
            account_id, card_number, card_type,
            expiry_date, cvv,
            credit_limit, withdrawal_limit
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (
            account_id,
            card_number,
            card_type,
            expiry,
            cvv,
            credit_limit,
            withdrawal_limit,
        ),
    )
    return row


def get_all_cards(branch_id: int) -> List[Dict[str, Any]]:
    """
    (21) Get all cards for accounts within a branch.
    """
    return fetch_all(
        """
        SELECT
            c.*,
            a.account_number,
            a.account_type
        FROM cards c
        JOIN accounts a ON c.account_id = a.account_id
        WHERE a.branch_id = %s
        ORDER BY c.issued_date DESC
        """,
        (branch_id,),
    )

