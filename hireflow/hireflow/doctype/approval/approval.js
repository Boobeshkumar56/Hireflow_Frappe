// Copyright (c) 2026, Boobesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Approval", {
	refresh(frm) {
        if(frm.doc.action=="Submitted" ||frm.doc.action=="Commented" ){
            frm.add_custom_button("Approve", ()=> {
                frappe.call({method:"hireflow.hireflow.doctype.approval.approval.approve",
                    args:{approval:frm.doc.name},
                    callback:(r)=>{
                    frm.reload_doc()
                }})
            }).addClass('btn-primary')
            
            frm.add_custom_button("Decline", () => {
                frappe.call({
                    method: "hireflow.hireflow.doctype.approval.approval.reject",
                    args: {
                        approval: frm.doc.name
                    },
                    callback: function(r) {
                        frm.reload_doc();
                    }
                });
            }).addClass('btn-danger');
        if(frm.doc.action!="Commented")
        frm.add_custom_button("Comment", () => {
            const dialog = new frappe.ui.Dialog({
                title: "Add Comment",
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
                        method: "hireflow.hireflow.doctype.approval.approval.add_comment",
                        args: {
                            approval: frm.doc.name,
                            comment: values.comment
                        }
                    }).then(() => {

                        dialog.hide();
                        frm.reload_doc();

                    });
                }
            });

            dialog.show();
        }).addClass('btn-secondary');
        }

         
    }


	},

        
);
