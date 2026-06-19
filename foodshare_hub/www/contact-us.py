import frappe


def get_context(context):
    """Get context for contact-us page."""
    context.no_cache = 1
    context.title = "Contact Us - FoodShare Hub"
