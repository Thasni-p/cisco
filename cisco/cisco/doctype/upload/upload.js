// Copyright (c) 2024, thasni and contributors
// For license information, please see license.txt
frappe.ui.form.on("CDR Upload", {
	refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("Process CDR"), function() {
                frappe.call ({
                    method: 'cisco.cisco.doctype.cdr_upload.cdr_upload.process_cdr',
                    args : {doc_id : frm.doc.name},
                    callback: function() {
                        frm.reload_doc();
                    }
                });
            });
        }
	},
    from_date(frm) {
        if (frm.doc.to_date && frm.doc.to_date < frm.doc.from_date) {
            frappe.msgprint(__('From Date must be less than To Date.'));
            frm.set_value('from_date', '')
        }
    },
    to_date(frm) {
        if (frm.doc.from_date && frm.doc.to_date < frm.doc.from_date) {
            frappe.msgprint(__('To Date must be greater than From Date.'));
            frm.set_value('to_date', '')
        }
    }
});
