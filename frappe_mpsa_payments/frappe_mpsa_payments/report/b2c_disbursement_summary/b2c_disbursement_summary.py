# Copyright (c) 2025, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label":_("ID"), "fieldname":"name"},
        {"label":_("Party Type"), "fieldname":"party_type", "fieldtype":"Select"},
        {"label":_("Posting Date"), "fieldname":"posting_date", "fieldtype":"Date"},
        {"label":_("Amount"), "fieldname":"paid_amount", "fieldtype":"Currency"},
        {"label":_("Transaction"), "fieldname":"transaction_to_pay_against", "fieldtype":"Link"},
        {"label":_("Status"), "fieldname":"status", "fieldtype":"Select"},
        {"label":_("Payment Type"), "fieldname":"payment_type", "fieldtype":"Link"},
        {"label":_("Company"), "fieldname":"company", "fieldtype":"Link"},
        {"label":_("Company currency"), "fieldname":"company_currency", "fieldtype":"Link"},
        {"label":_("Account Paid From"), "fieldname":"paid_from", "fieldtype":"Link"},
        {"label":_("Account Paid To"), "fieldname":"paid_to", "fieldtype":"Link"}
    ]


def generate_columns_for_doctype(doctype):
    meta = frappe.get_meta(doctype)
    columns = []

    for field in meta.fields:
        if field.fieldtype not in ("Section Break", "Column Break", "Fold", ""):
            column = {
                "label": field.label,
                "fieldname": field.fieldname,
                "fieldtype": field.fieldtype
            }

            if field.fieldtype in ("Link", "Select", "Table"):
                column["options"] = field.options or ""

            columns.append(column)

    columns.insert(0, {
        "label": "Name",
        "fieldname": "name",
        "fieldtype": "Link",
        "options": doctype
    })

    return columns


def get_data(filters):
    """
    Build WHERE clauses only for filters the user actually filled in.
    All values are passed through the `values` dict → safe, parametrised SQL.
    """
    conditions = []
    values = {}

    # ----- 1. Party Type (Link to DocType) -----
    if filters.get("party_type"):
        conditions.append("party_type = %(party_type)s")
        values["party_type"] = filters["party_type"]

    # ----- 2. Posting Date
    if filters.get("posting_date"):
        conditions.append("posting_date = %(posting_date)s")
        values["posting_date"] = filters["posting_date"]

    # ----- 3. Transaction to Pay Against -----
    if filters.get("transaction_to_pay_against"):
        conditions.append("transaction_to_pay_against = %(tx)s")
        values["tx"] = filters["transaction_to_pay_against"]

    where_clause = " AND ".join(conditions) if conditions else "1 = 1"

    return frappe.db.sql(
        f"""
            SELECT
                name,
                payment_type,
                company,
                company_currency,
                paid_from,
                party_type,
                posting_date,
                paid_amount,
                transaction_to_pay_against,
                status
            FROM `tabB2C Payment Disbursement`
            WHERE {where_clause}
            ORDER BY creation DESC
        """,
        values,
        as_dict=True,
    )



