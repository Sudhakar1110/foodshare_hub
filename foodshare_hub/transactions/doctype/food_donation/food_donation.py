import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime


class FoodDonation(Document):
    """Food Donation Transaction Document."""

    website = frappe._dict(
        condition_field="status",
        condition_value="Available",
        page_title_field="donor",
    )
    
    def validate(self):
        """Validate Food Donation."""
        self.validate_dates()
        self.validate_quantity()
    
    def validate_dates(self):
        """Validate pickup and expiry dates."""
        if self.pickup_datetime and self.expiry_datetime:
            pickup = get_datetime(self.pickup_datetime)
            expiry = get_datetime(self.expiry_datetime)
            if expiry <= pickup:
                frappe.throw("Expiry Date & Time must be after Pickup Date & Time.")
    
    def validate_quantity(self):
        """Validate quantity is positive."""
        if self.quantity <= 0:
            frappe.throw("Quantity must be greater than zero.")
    
    def on_update(self):
        """On update handler."""
        pass
    
    def after_insert(self):
        """After insert handler."""
        pass


def validate_dates(doc, method):
    """Validate dates hook handler."""
    if doc.expiry_datetime and doc.pickup_datetime:
        expiry = get_datetime(doc.expiry_datetime)
        pickup = get_datetime(doc.pickup_datetime)
        if expiry <= pickup:
            frappe.throw("Expiry Date & Time must be after Pickup Date & Time.")
