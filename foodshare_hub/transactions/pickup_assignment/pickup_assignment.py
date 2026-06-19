import frappe
from frappe.model.document import Document


class PickupAssignment(Document):
    """Pickup Assignment Transaction Document."""
    
    def validate(self):
        """Validate Pickup Assignment."""
        self.validate_donation_status()
        self.validate_volunteer_availability()
    
    def validate_donation_status(self):
        """Ensure donation is available for pickup."""
        if self.food_donation:
            donation = frappe.get_doc("Food Donation", self.food_donation)
            if donation.status != "Available":
                frappe.throw(f"Food Donation '{self.food_donation}' is not available for pickup. Current status: {donation.status}")
    
    def validate_volunteer_availability(self):
        """Ensure volunteer is active."""
        if self.volunteer:
            volunteer = frappe.get_doc("Volunteer", self.volunteer)
            if volunteer.status != "Active":
                frappe.throw(f"Volunteer '{self.volunteer}' is not active. Current status: {volunteer.status}")
    
    def on_update(self):
        """On update handler - update donation status."""
        if self.pickup_status == "Completed":
            donation = frappe.get_doc("Food Donation", self.food_donation)
            donation.db_set("status", "Collected")
