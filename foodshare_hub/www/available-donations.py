import frappe


def get_context(context):
    """Get context for available-donations page."""
    context.no_cache = 1
    context.title = "Available Donations - FoodShare Hub"
    
    # Get all available donations
    context.donations = frappe.get_all(
        "Food Donation",
        filters={"status": "Available"},
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
        order_by="pickup_datetime asc"
    )
