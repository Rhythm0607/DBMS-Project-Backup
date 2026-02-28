"""
BankBase backend function package.

This package groups the domain modules that implement all
database-backed operations used by the Flask app.
"""

from . import customer_core  # noqa: F401
from . import customer_extended  # noqa: F401
from . import employee_management  # noqa: F401
from . import employee_loans_cards  # noqa: F401
from . import db_helpers  # noqa: F401
from . import reports  # noqa: F401

