import frappe
from frappe import _


@frappe.whitelist()
def get_request(name):
    """Get a food request by name.
    
    Args:
        name: Request name
    
    Returns:
        Request document
    """
    if not frappe.has_permission("Food Request", "read"):
        frappe.throw(_("You don't have permission to view requests."), frappe.PermissionError)
    
    return frappe.get_doc("Food Request", name)


@frappe.whitelist()
def get_requests_by_receiver(receiver, status=None):
    """Get requests by receiver.
    
    Args:
        receiver: Receiver name
        status: Optional status filter
    
    Returns:
        List of requests
    """
    filters = {"receiver": receiver}
    
    if status:
        filters["status"] = status
    
    return frappe.get_all(
        "Food Request",
        filters=filters,
        fields=["*"],
        order_by="creation desc"
    )


@frappe.whitelist()
def update_request_status(name, status):
    """Update request status.
    
    Args:
        name: Request name
        status: New status
    
    Returns:
        Updated request
    """
    if not frappe.has_permission("Food Request", "write"):
        frappe.throw(_("You don't have permission to update requests."), frappe.PermissionError)
    
    doc = frappe.get_doc("Food Request", name)
    doc.status = status
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    
    return doc


@frappe.whitelist()
def get_pending_requests_count():
    """Get count of pending requests.
    
    Returns:
        Count of pending requests
    """
    return frappe.db.count("Food Request", {"status": "Submitted"})
