// FoodShare Hub - Public JavaScript
// Add any public-facing JavaScript here

frappe.ready(function() {
    console.log("FoodShare Hub loaded");
});

// FoodShare Hub namespace
var FoodShareHub = FoodShareHub || {};

FoodShareHub.utils = {
    // Format date for display
    formatDate: function(dateString) {
        if (!dateString) return '';
        var date = new Date(dateString);
        return date.toLocaleDateString();
    },
    
    // Format datetime for display
    formatDateTime: function(dateTimeString) {
        if (!dateTimeString) return '';
        var date = new Date(dateTimeString);
        return date.toLocaleString();
    },
    
    // Get status color class
    getStatusClass: function(status) {
        var statusMap = {
            'Draft': 'secondary',
            'Available': 'success',
            'Collected': 'info',
            'Expired': 'warning',
            'Submitted': 'primary',
            'Approved': 'success',
            'Fulfilled': 'info',
            'Rejected': 'danger',
            'Pending': 'secondary',
            'In Progress': 'warning',
            'In Transit': 'info',
            'Delivered': 'success',
            'Failed': 'danger',
            'Cancelled': 'dark'
        };
        return statusMap[status] || 'secondary';
    }
};
