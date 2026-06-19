frappe.ui.form.on('Food Request', {
    refresh(frm) {
        // Add custom actions
        if (frm.doc.status === 'Draft') {
            frm.add_custom_button(__('Submit'), () => {
                frm.set_value('status', 'Submitted');
                frm.save();
            });
        }
        
        if (frm.doc.status === 'Submitted') {
            frm.add_custom_button(__('Approve'), () => {
                frm.set_value('status', 'Approved');
                frm.save();
            });
            
            frm.add_custom_button(__('Reject'), () => {
                frm.set_value('status', 'Rejected');
                frm.save();
            });
        }
        
        if (frm.doc.status === 'Approved') {
            frm.add_custom_button(__('Mark Fulfilled'), () => {
                frm.set_value('status', 'Fulfilled');
                frm.save();
            });
        }
    },
    
    receiver(frm) {
        // Auto-fill delivery address from receiver
        if (frm.doc.receiver) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Receiver',
                    name: frm.doc.receiver
                },
                callback: function(r) {
                    if (r.message && r.message.address) {
                        frm.set_value('delivery_address', r.message.address);
                    }
                }
            });
        }
    }
});
