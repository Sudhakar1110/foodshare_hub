frappe.ui.form.on('Food Donation', {
    refresh(frm) {
        // Add custom actions
        if (frm.doc.status === 'Draft') {
            frm.add_custom_button(__('Make Available'), () => {
                frm.set_value('status', 'Available');
                frm.save();
            });
        }
        
        if (frm.doc.status === 'Available') {
            frm.add_custom_button(__('Mark Collected'), () => {
                frm.set_value('status', 'Collected');
                frm.save();
            });
        }
    },
    
    pickup_datetime(frm) {
        // Auto-calculate expiry if needed
        if (frm.doc.pickup_datetime && !frm.doc.expiry_datetime) {
            frappe.call({
                method: 'frappe.utils.add_to_date',
                args: {
                    date: frm.doc.pickup_datetime,
                    hours: 24
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('expiry_datetime', r.message);
                    }
                }
            });
        }
    },
    
    donor(frm) {
        // Auto-fill donor details if needed
        if (frm.doc.donor) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Donor',
                    name: frm.doc.donor
                },
                callback: function(r) {
                    if (r.message && r.message.address) {
                        frm.set_value('pickup_address', r.message.address);
                    }
                }
            });
        }
    }
});
