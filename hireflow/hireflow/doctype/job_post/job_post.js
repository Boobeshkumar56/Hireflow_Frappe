// Copyright (c) 2026, Boobesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Post", {
	refresh(frm) {
        frm.add_custom_button("Apply Job",()=>{
            console.log("Job applied successfulyy")
        })
	},

});
