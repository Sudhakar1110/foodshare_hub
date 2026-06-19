import json
import os

import frappe
from frappe.utils import now_datetime


def after_install():
    """Run tasks after app installation."""
    load_demo_data()


def after_migrate():
    """Run tasks after app migration."""
    pass


def load_demo_data():
    """Load demo data from demo_data.json fixture file."""
    demo_data_path = frappe.get_app_path("foodshare_hub", "fixtures", "demo_data.json")

    if not os.path.exists(demo_data_path):
        return

    with open(demo_data_path) as f:
        demo_records = json.load(f)

    for record_data in demo_records:
        doctype = record_data.get("doctype")
        if not doctype:
            continue

        # Skip if record already exists
        # Determine the title field based on doctype
        title_field_map = {
            "Food Category": "category_name",
            "Donor Organization": "organization_name",
            "NGO Partner": "ngo_name",
            "Donor": "donor_name",
            "Receiver": "receiver_name",
            "Volunteer": "volunteer_name",
        }

        title_field = title_field_map.get(doctype)
        title_value = record_data.get(title_field) if title_field else None

        if title_field and title_value:
            if frappe.db.exists(doctype, {title_field: title_value}):
                continue

        try:
            doc = frappe.get_doc(record_data)
            doc.insert(ignore_permissions=True)
        except Exception:
            frappe.log_error(
                message=f"Failed to create demo {doctype}: {frappe.get_traceback()}",
                title=f"FoodShare Hub Demo Data - {doctype}",
            )

    frappe.db.commit()
