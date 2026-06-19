import frappe
from frappe import _


def update_modified(doc, method):
    """Update modified timestamp on related documents."""
    pass


@frappe.whitelist()
def get_available_donations(food_category=None, limit=20):
    """Get available food donations.
    
    Args:
        food_category: Optional filter by food category
        limit: Maximum number of results
    
    Returns:
        List of available donations
    """
    filters = {"status": "Available"}
    
    if food_category:
        filters["food_category"] = food_category
    
    donations = frappe.get_all(
        "Food Donation",
        filters=filters,
        fields=[
            "name",
            "donor",
            "food_category",
            "food_description",
            "quantity",
            "unit",
            "pickup_datetime",
            "expiry_datetime",
            "pickup_address"
        ],
        order_by="pickup_datetime asc",
        limit=limit
    )
    
    return donations


@frappe.whitelist()
def get_pending_requests(food_category=None, priority=None, limit=20):
    """Get pending food requests.
    
    Args:
        food_category: Optional filter by food category
        priority: Optional filter by priority
        limit: Maximum number of results
    
    Returns:
        List of pending requests
    """
    filters = {"status": "Submitted"}
    
    if food_category:
        filters["food_category"] = food_category
    
    if priority:
        filters["priority"] = priority
    
    requests = frappe.get_all(
        "Food Request",
        filters=filters,
        fields=[
            "name",
            "receiver",
            "food_category",
            "required_quantity",
            "unit",
            "request_date",
            "delivery_date",
            "priority",
            "status"
        ],
        order_by="priority desc, request_date asc",
        limit=limit
    )
    
    return requests


@frappe.whitelist()
def create_donation(donor, food_category, food_description, quantity, unit, 
                    pickup_datetime, expiry_datetime, pickup_address=None):
    """Create a new food donation.
    
    Args:
        donor: Donor name
        food_category: Food category
        food_description: Description of food
        quantity: Quantity
        unit: Unit of measurement
        pickup_datetime: Pickup date and time
        expiry_datetime: Expiry date and time
        pickup_address: Pickup address
    
    Returns:
        Created donation document name
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("You must be logged in to create a donation."), frappe.PermissionError)
    
    doc = frappe.get_doc({
        "doctype": "Food Donation",
        "donor": donor,
        "food_category": food_category,
        "food_description": food_description,
        "quantity": quantity,
        "unit": unit,
        "pickup_datetime": pickup_datetime,
        "expiry_datetime": expiry_datetime,
        "pickup_address": pickup_address,
        "status": "Draft"
    })
    
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    return {"name": doc.name, "status": doc.status}


@frappe.whitelist()
def create_request(receiver, food_category, required_quantity, unit, 
                   request_date, delivery_date=None, delivery_address=None, 
                   priority="Medium"):
    """Create a new food request.
    
    Args:
        receiver: Receiver name
        food_category: Food category
        required_quantity: Required quantity
        unit: Unit of measurement
        request_date: Request date
        delivery_date: Preferred delivery date
        delivery_address: Delivery address
        priority: Priority level
    
    Returns:
        Created request document name
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("You must be logged in to create a request."), frappe.PermissionError)
    
    doc = frappe.get_doc({
        "doctype": "Food Request",
        "receiver": receiver,
        "food_category": food_category,
        "required_quantity": required_quantity,
        "unit": unit,
        "request_date": request_date,
        "delivery_date": delivery_date,
        "delivery_address": delivery_address,
        "priority": priority,
        "status": "Draft"
    })
    
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    return {"name": doc.name, "status": doc.status}


@frappe.whitelist()
def get_donation_stats():
    """Get statistics about food donations.
    
    Returns:
        Dictionary with donation statistics
    """
    stats = {
        "total_donations": frappe.db.count("Food Donation"),
        "available_donations": frappe.db.count("Food Donation", {"status": "Available"}),
        "collected_donations": frappe.db.count("Food Donation", {"status": "Collected"}),
        "expired_donations": frappe.db.count("Food Donation", {"status": "Expired"}),
        "total_quantity_donated": frappe.db.sql("""
            SELECT COALESCE(SUM(quantity), 0) as total 
            FROM `tabFood Donation` 
            WHERE status = 'Collected'
        """, as_dict=True)[0].total
    }
    
    return stats


@frappe.whitelist()
def get_request_stats():
    """Get statistics about food requests.
    
    Returns:
        Dictionary with request statistics
    """
    stats = {
        "total_requests": frappe.db.count("Food Request"),
        "pending_requests": frappe.db.count("Food Request", {"status": "Submitted"}),
        "approved_requests": frappe.db.count("Food Request", {"status": "Approved"}),
        "fulfilled_requests": frappe.db.count("Food Request", {"status": "Fulfilled"}),
        "rejected_requests": frappe.db.count("Food Request", {"status": "Rejected"})
    }
    
    return stats
