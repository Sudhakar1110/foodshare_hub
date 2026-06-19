frappe.ui.form.on('Pickup Assignment', {
    refresh(frm) {
        // Add custom actions
        if (frm.doc.pickup_status === 'Pending') {
            frm.add_custom_button(__('Start Pickup'), () => {
                frm.set_value('pickup_status', 'In Progress');
                frm.save();
            });
        }
        
        if (frm.doc.pickup_status === 'In Progress') {
            frm.add_custom_button(__('Complete Pickup'), () => {
                frm.set_value('pickup_status', 'Completed');
                frm.save();
            });
        }
        
        if (frm.doc.pickup_status !== 'Completed') {
            frm.add_custom_button(__('Cancel Pickup'), () => {
                frm.set_value('pickup_status', 'Cancelled');
                frm.save();
            });
        }
    },
    
    volunteer(frm) {
        // Auto-fill volunteer phone
        if (frm.doc.volunteer) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Volunteer',
                    name: frm.doc.volunteer
                },
                callback: function(r) {
                    if (r.message && r.message.phone) {
                        frm.set_value('contact_phone', r.message.phone);
                    }
                }
            });
        }
    },
    
    food_donation(frm) {
        // Auto-fill pickup date from donation
        if (frm.doc.food_donation) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Food Donation',
                    name: frm.doc.food_donation
                },
                callback: function(r) {
                    if (r.message && r.message.pickup_datetime) {
                        // Extract date from datetime
                        var pickupDate = r.message.pickup_datetime.split(' ')[0];
                        frm.set_value('pickup_date', pickupDate);
                    }
                }
            });
        }
    }
});
