# Copyright (c) 2024, FoodShare Hub and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """Execute the Food Donation Report."""
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    """Return columns for the report."""
    return [
        {
            "fieldname": "donation_id",
            "label": _("Donation ID"),
            "fieldtype": "Link",
            "options": "Food Donation",
            "width": 120,
        },
        {
            "fieldname": "donor",
            "label": _("Donor"),
            "fieldtype": "Link",
            "options": "Donor",
            "width": 150,
        },
        {
            "fieldname": "food_category",
            "label": _("Food Category"),
            "fieldtype": "Link",
            "options": "Food Category",
            "width": 120,
        },
        {
            "fieldname": "food_description",
            "label": _("Description"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "quantity",
            "label": _("Quantity"),
            "fieldtype": "Float",
            "width": 80,
        },
        {
            "fieldname": "unit",
            "label": _("Unit"),
            "fieldtype": "Data",
            "width": 60,
        },
        {
            "fieldname": "pickup_datetime",
            "label": _("Pickup Date & Time"),
            "fieldtype": "Datetime",
            "width": 150,
        },
        {
            "fieldname": "expiry_datetime",
            "label": _("Expiry Date & Time"),
            "fieldtype": "Datetime",
            "width": 150,
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Select",
            "width": 100,
        },
    ]


def get_data(filters=None):
    """Return data for the report."""
    conditions = get_conditions(filters)

    query = """\
        SELECT
            name as donation_id,
            donor,
            food_category,
            food_description,
            quantity,
            unit,
            pickup_datetime,
            expiry_datetime,
            status
        FROM `tabFood Donation`
        WHERE 1=1 {conditions}
        ORDER BY creation DESC
    """.format(conditions=conditions)

    return frappe.db.sql(query, filters, as_dict=1)


def get_conditions(filters=None):
    """Build query conditions based on filters."""
    conditions = []

    if filters:
        if filters.get("donor"):
            conditions.append("AND donor = %(donor)s")
        if filters.get("food_category"):
            conditions.append("AND food_category = %(food_category)s")
        if filters.get("status"):
            conditions.append("AND status = %(status)s")
        if filters.get("from_date"):
            conditions.append("AND pickup_datetime >= %(from_date)s")
        if filters.get("to_date"):
            conditions.append("AND pickup_datetime <= %(to_date)s")

    return " ".join(conditions)
