# Copyright (c) 2024, FoodShare Hub and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """Execute the Food Request Report."""
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    """Return columns for the report."""
    return [
        {
            "fieldname": "request_id",
            "label": _("Request ID"),
            "fieldtype": "Link",
            "options": "Food Request",
            "width": 120
        },
        {
            "fieldname": "receiver",
            "label": _("Receiver"),
            "fieldtype": "Link",
            "options": "Receiver",
            "width": 150
        },
        {
            "fieldname": "food_category",
            "label": _("Food Category"),
            "fieldtype": "Link",
            "options": "Food Category",
            "width": 120
        },
        {
            "fieldname": "required_quantity",
            "label": _("Required Quantity"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "unit",
            "label": _("Unit"),
            "fieldtype": "Data",
            "width": 60
        },
        {
            "fieldname": "request_date",
            "label": _("Request Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "delivery_date",
            "label": _("Preferred Delivery Date"),
            "fieldtype": "Date",
            "width": 150
        },
        {
            "fieldname": "priority",
            "label": _("Priority"),
            "fieldtype": "Select",
            "width": 80
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Select",
            "width": 100
        }
    ]


def get_data(filters=None):
    """Return data for the report."""
    conditions = get_conditions(filters)
    
    query = """
        SELECT 
            name as request_id,
            receiver,
            food_category,
            required_quantity,
            unit,
            request_date,
            delivery_date,
            priority,
            status
        FROM `tabFood Request`
        WHERE 1=1 {conditions}
        ORDER BY creation DESC
    """.format(conditions=conditions)
    
    return frappe.db.sql(query, filters, as_dict=1)


def get_conditions(filters=None):
    """Build query conditions based on filters."""
    conditions = []
    
    if filters:
        if filters.get("receiver"):
            conditions.append("AND receiver = %(receiver)s")
        if filters.get("food_category"):
            conditions.append("AND food_category = %(food_category)s")
        if filters.get("status"):
            conditions.append("AND status = %(status)s")
        if filters.get("priority"):
            conditions.append("AND priority = %(priority)s")
        if filters.get("from_date"):
            conditions.append("AND request_date >= %(from_date)s")
        if filters.get("to_date"):
            conditions.append("AND request_date <= %(to_date)s")
    
    return " ".join(conditions)
