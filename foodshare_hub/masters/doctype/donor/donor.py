import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address


class Donor(Document):
    """Donor Master Document."""
    
    def validate(self):
        """Validate Donor."""
        self.validate_email()
        self.validate_phone()
    
    def validate_email(self):
        """Validate email format if provided."""
        if self.email:
            validate_email_address(self.email, throw=True)
    
    def validate_phone(self):
        """Validate phone number if provided."""
        if self.phone and len(self.phone.strip()) < 10:
            frappe.throw("Please enter a valid phone number.")
