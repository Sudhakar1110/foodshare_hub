frappe.ui.form.on('Delivery Tracking', {
    refresh(frm) {
        // Add custom actions
        if (frm.doc.delivery_status === 'Pending') {
            frm.add_custom_button(__('Start Delivery'), () => {
                frm.set_value('delivery_status', 'In Transit');
                frm.save();
            });
        }
        
        if (frm.doc.delivery_status === 'In Transit') {
            frm.add_custom_button(__('Mark Delivered'), () => {
                frm.set_value('delivery_status', 'Delivered');
                frm.save();
            });
            
            frm.add_custom_button(__('Mark Failed'), () => {
                frm.set_value('delivery_status', 'Failed');
                frm.save();
            });
        }
    },
    
    pickup_assignment(frm) {
        // Auto-fill details from pickup assignment
        if (frm.doc.pickup_assignment) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Pickup Assignment',
                    name: frm.doc.pickup_assignment
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('food_donation', r.message.food_donation);
                    }
                }
            });
        }
    },
    
    receiver(frm) {
        // Auto-fill receiver contact
        if (frm.doc.receiver) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Receiver',
                    name: frm.doc.receiver
                },
                callback: function(r) {
                    if (r.message) {
                        if (r.message.phone) {
                            frm.set_value('receiver_contact', r.message.phone);
                        }
                        if (r.message.address) {
                            frm.set_value('delivery_address', r.message.address);
                        }
                    }
                }
            });
        }
    }
});
