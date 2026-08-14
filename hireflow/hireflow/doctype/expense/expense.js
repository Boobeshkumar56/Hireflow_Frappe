// Copyright (c) 2026, Boobesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense", {
	onload(frm){
        if(!frm.is_new()){
            return;
        }
        frappe.call({
            method:"hireflow.api.get_empid",
            callback: function(r) {
                if(!r.message){
                    frappe.throw("Employee Not Found")
                    return
                }
                frm.set_value("employee_id", r.message)
                    return;


                
            }
        })
    },
});
