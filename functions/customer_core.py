"""
Customer core operations (functions 1–5).

These functions encapsulate login, dashboard aggregation and basic
customer-facing data fetches.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import bcrypt

from db import fetch_one, fetch_all


def verify_customer_login(mobile: str, password: str) -> Optional[Dict[str, Any]]:
    """
    (1) Verify customer login with mobile + password.

    Returns the customer row (without password_hash) on success,
    or None on failure.
    """
    customer = fetch_one(
        "SELECT * FROM customers WHERE mobile = %s",
        (mobile,),
    )
    if not customer:
        return None

    # For this project/demo, accept a fixed password string ("password")
    # for all customers instead of verifying the stored hash.
    if password != "password":
        return None

    # Do not leak the hash further in the app
    customer = dict(customer)
    customer.pop("password_hash", None)
    return customer


def get_customer_profile(customer_id: int) -> Optional[Dict[str, Any]]:
    """
    (3) Fetch basic customer profile details.
    """
    return fetch_one(
        "SELECT * FROM customers WHERE customer_id = %s",
        (customer_id,),
    )


def get_customer_accounts(customer_id: int) -> List[Dict[str, Any]]:
    """
    (5) Fetch all accounts that belong to a customer.
    """
    return fetch_all(
        """
        SELECT
            a.*,
            b.branch_name,
            b.ifsc_code
        FROM accounts a
        JOIN branches b ON a.branch_id = b.branch_id
        WHERE a.customer_id = %s
        ORDER BY a.opened_at ASC
        """,
        (customer_id,),
    )


def get_transaction_history(
    account_id: int,
    limit: int = 50,
    date_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    (4) Get transaction history for an account.

    - `limit` controls how many rows to fetch (most recent first)
    - If `date_filter` is provided (YYYY-MM-DD), only rows with
      created_at::date >= date_filter are returned.
    """
    params: list[Any] = [account_id]
    where_clauses = ["t.account_id = %s"]

    if date_filter:
        where_clauses.append("t.created_at::date >= %s")
        params.append(date_filter)

    params.append(limit)

    sql = f"""
        SELECT
            t.tx_id,
            t.tx_type,
            t.amount,
            t.balance_after,
            t.related_account,
            t.created_at,
            t.description
        FROM transactions t
        WHERE {" AND ".join(where_clauses)}
        ORDER BY t.created_at DESC, t.tx_id DESC
        LIMIT %s
    """

    return fetch_all(sql, tuple(params))


def get_customer_dashboard(customer_id: int) -> Dict[str, Any]:
    """
    (2) Return a dashboard summary for the customer.

    Includes:
    - total_accounts
    - total_balance
    - active_loans
    - cards_count
    - recent_transactions (last 5 across all accounts)
    """
    accounts = get_customer_accounts(customer_id)
    total_accounts = len(accounts)
    total_balance = sum(a["balance"] for a in accounts) if accounts else 0

    loans = fetch_all(
        "SELECT * FROM loans WHERE customer_id = %s AND status IN ('ACTIVE', 'PENDING')",
        (customer_id,),
    )
    cards = fetch_all(
        """
        SELECT c.*
        FROM cards c
        JOIN accounts a ON c.account_id = a.account_id
        WHERE a.customer_id = %s
        """,
        (customer_id,),
    )

    recent_tx = fetch_all(
        """
        SELECT
            t.tx_id,
            t.account_id,
            a.account_number,
            t.tx_type,
            t.amount,
            t.balance_after,
            t.created_at,
            t.description
        FROM transactions t
        JOIN accounts a ON t.account_id = a.account_id
        WHERE a.customer_id = %s
        ORDER BY t.created_at DESC, t.tx_id DESC
        LIMIT 5
        """,
        (customer_id,),
    )

    return {
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "active_loans": len(loans),
        "cards_count": len(cards),
        "recent_transactions": recent_tx,
    }

