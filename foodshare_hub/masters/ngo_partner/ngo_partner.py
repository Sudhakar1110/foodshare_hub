import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address


class NGOPartner(Document):
    """NGO Partner Master Document."""
    
    def validate(self):
        """Validate NGO Partner."""
        self.validate_email()
    
    def validate_email(self):
        """Validate email format if provided."""
        if self.email:
            validate_email_address(self.email, throw=True)
