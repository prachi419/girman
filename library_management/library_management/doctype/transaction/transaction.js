// Copyright (c) 2025, Orachi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Transaction", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Transaction', {
    refresh: function(frm) {
        if (frm.doc.status === "Issued" && !frm.doc.return_date) {
            frm.add_custom_button("Return Book", () => {
                frappe.call({
                    method: "frappe.client.set_value",
                    args: {
                        doctype: "Transaction",
                        name: frm.doc.name,
                        fieldname: {
                            status: "Returned",
                            return_date: frappe.datetime.get_today()
                        }
                    },
                    callback: () => {
                        frappe.msgprint("Book Returned");
                        frm.reload_doc();
                    }
                });
            });
        }
    }
});
