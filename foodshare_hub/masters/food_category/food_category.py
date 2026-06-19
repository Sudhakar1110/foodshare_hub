import frappe
from frappe.model.document import Document


class FoodCategory(Document):
    """Food Category Master Document."""
    
    def validate(self):
        """Validate Food Category."""
        self.validate_category_name()
    
    def validate_category_name(self):
        """Ensure category name is not empty or duplicate."""
        if not self.category_name:
            frappe.throw("Category Name is required.")
        
        if self.is_new():
            exists = frappe.db.exists("Food Category", {"category_name": self.category_name})
            if exists:
                frappe.throw(f"Food Category '{self.category_name}' already exists.")
