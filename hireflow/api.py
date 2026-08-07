import frappe
def success_message(doc,method):
    frappe.msgprint(f"New {doc.doctype} document with id {doc.name} saved successfully")

@frappe.whitelist()
def get_applicant_details():
    from frappe.query_builder import DocType
    applicant=DocType("Applicant")
    applications=DocType("Job Applications")
    query=(frappe.qb.from_(applicant)
           .join(applications)
           .on(applicant.name==applications.applicant)
           .select(applicant.name1,applicant.contact,applicant.email,applications.applicant,applications.name.as_("application_name")))

    results=query.run(as_dict=True)
    applicant_id=results[0]["application_name"]
    print(applicant_id)
    applicant_1=frappe.get_doc("Job Applications",applicant_id)
    frappe.db.set_value("Job Applications",applicant_id,"verified",1)
    frappe.db.commit()
    return applicant_1.reload()
