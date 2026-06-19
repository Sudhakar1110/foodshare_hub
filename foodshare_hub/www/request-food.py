import frappe


def get_context(context):
    """Get context for request-food page."""
    context.no_cache = 1
    context.title = "Request Food - FoodShare Hub"
