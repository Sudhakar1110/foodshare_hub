import frappe


def get_context(context):
    """Get context for home page."""
    context.no_cache = 1
    context.title = "FoodShare Hub - Sharing Food, Spreading Hope"
    
    # Get available donations count
    context.donations_count = frappe.db.count("Food Donation", {"status": "Available"})
    context.requests_count = frappe.db.count("Food Request", {"status": "Submitted"})
    
    # Get recent donations
    context.recent_donations = frappe.get_all(
        "Food Donation",
        filters={"status": "Available"},
        fields=["name", "food_category", "quantity", "unit", "pickup_datetime"],
        order_by="creation desc",
        limit=5
    )
