import frappe
from frappe.model.document import Document


class FoodRequest(Document):
    """Food Request Transaction Document."""
    
    def validate(self):
        """Validate Food Request."""
        self.validate_quantity()
        self.validate_dates()
    
    def validate_quantity(self):
        """Validate quantity is positive."""
        if self.required_quantity <= 0:
            frappe.throw("Required Quantity must be greater than zero.")
    
    def validate_dates(self):
        """Validate request and delivery dates."""
        if self.request_date and self.delivery_date:
            if self.delivery_date < self.request_date:
                frappe.throw("Preferred Delivery Date cannot be before Request Date.")
