import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address


class DonorOrganization(Document):
    """Donor Organization Master Document."""
    
    def validate(self):
        """Validate Donor Organization."""
        self.validate_contact_email()
    
    def validate_contact_email(self):
        """Validate email format if provided."""
        if self.contact_email:
            validate_email_address(self.contact_email, throw=True)
