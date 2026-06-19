import frappe
from frappe import _


@frappe.whitelist()
def get_donation(name):
    """Get a food donation by name.
    
    Args:
        name: Donation name
    
    Returns:
        Donation document
    """
    if not frappe.has_permission("Food Donation", "read"):
        frappe.throw(_("You don't have permission to view donations."), frappe.PermissionError)
    
    return frappe.get_doc("Food Donation", name)


@frappe.whitelist()
def get_donations_by_donor(donor, status=None):
    """Get donations by donor.
    
    Args:
        donor: Donor name
        status: Optional status filter
    
    Returns:
        List of donations
    """
    filters = {"donor": donor}
    
    if status:
        filters["status"] = status
    
    return frappe.get_all(
        "Food Donation",
        filters=filters,
        fields=["*"],
        order_by="creation desc"
    )


@frappe.whitelist()
def update_donation_status(name, status):
    """Update donation status.
    
    Args:
        name: Donation name
        status: New status
    
    Returns:
        Updated donation
    """
    if not frappe.has_permission("Food Donation", "write"):
        frappe.throw(_("You don't have permission to update donations."), frappe.PermissionError)
    
    doc = frappe.get_doc("Food Donation", name)
    doc.status = status
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    
    return doc


@frappe.whitelist()
def get_available_donations_count():
    """Get count of available donations.
    
    Returns:
        Count of available donations
    """
    return frappe.db.count("Food Donation", {"status": "Available"})
