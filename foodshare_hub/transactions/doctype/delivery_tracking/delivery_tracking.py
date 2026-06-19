import frappe
from frappe.model.document import Document


class DeliveryTracking(Document):
    """Delivery Tracking Transaction Document."""
    
    def validate(self):
        """Validate Delivery Tracking."""
        self.validate_pickup_completed()
        self.validate_receiver_active()
    
    def validate_pickup_completed(self):
        """Ensure pickup is completed before delivery."""
        if self.pickup_assignment:
            pickup = frappe.get_doc("Pickup Assignment", self.pickup_assignment)
            if pickup.pickup_status != "Completed":
                frappe.throw(f"Pickup Assignment '{self.pickup_assignment}' must be completed before delivery. Current status: {pickup.pickup_status}")
    
    def validate_receiver_active(self):
        """Ensure receiver is active."""
        if self.receiver:
            receiver = frappe.get_doc("Receiver", self.receiver)
            if receiver.status != "Active":
                frappe.throw(f"Receiver '{self.receiver}' is not active. Current status: {receiver.status}")
