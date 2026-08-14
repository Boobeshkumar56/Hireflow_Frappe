// Copyright (c) 2026, Boobesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Finance Ticket", {
	async refresh(frm) {
     const r=await frappe.call({
        method:"hireflow.api.employee_dept"
     })
     frm.department=r.message;
        if(frm.doc.status=="Opened" && frm.department=='FINANCE'){
        frm.add_custom_button("Approve", ()=>{
            frappe.call({
                method: "hireflow.hireflow.doctype.finance_ticket.finance_ticket.approve_expense_ticket",
                args:{
                    finance:frm.doc.name
                },
                callback: function(r) {
                    frm.reload_doc()
                }
            })
        }).addClass("btn-success");
        
         frm.add_custom_button("Reject", ()=>{
             const dialog = new frappe.ui.Dialog({
                title: "Reason for rejection",
                fields: [
                    {
                        fieldname: "comment",
                        label: "Comment",
                        fieldtype: "Small Text",
                        reqd: 1
                    }
                ],
                primary_action_label: "Submit",

                primary_action(values) {

                    frappe.call({
                        method: "hireflow.hireflow.doctype.finance_ticket.finance_ticket.reject_expense_ticket",
                        args: {
                            finance: frm.doc.name,
                            reason: values.comment
                        }
                    }).then(() => {

                        dialog.hide();
                        frm.reload_doc();

                    });
                }
            });

            dialog.show();
        }).addClass("btn-danger");}

	},
});
