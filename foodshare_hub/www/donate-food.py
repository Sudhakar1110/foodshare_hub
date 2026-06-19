import frappe


def get_context(context):
    """Get context for donate-food page."""
    context.no_cache = 1
    context.title = "Donate Food - FoodShare Hub"
