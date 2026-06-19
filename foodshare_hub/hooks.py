app_name = "foodshare_hub"
app_title = "FoodShare Hub"
app_publisher = "FoodShare Hub"
app_description = "Leftover Food Sharing Platform"
app_email = "admin@foodsharehub.com"
app_license = "MIT"
app_version = "1.0.0"

fixtures = [
    "Role",
    "Custom DocPerm",
    "Workflow",
    "Workflow State",
    "Workspace",
    "Property Setter"
]

doc_events = {
    "Food Donation": {
        "validate": "foodshare_hub.transactions.doctype.food_donation.food_donation.validate_dates"
    },
    "*": {
        "on_update": "foodshare_hub.api.utils.update_modified",
    }
}

website_route_rules = [
    {"from_route": "/donate", "to_route": "donate-food"},
    {"from_route": "/request", "to_route": "request-food"},
    {"from_route": "/available-donations", "to_route": "available-donations"},
    {"from_route": "/contact-us", "to_route": "contact-us"}
]

website_context = {
    "base_template_path": "templates/web.html",
    "website_route": "/"
}

app_include_js = []
app_include_css = []

web_include_css = []
web_include_js = []

def get_help_contents():
    return []

permission_query_conditions = {}

has_permission = {}

scheduler_events = {}
