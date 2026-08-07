import frappe
def success_message(doc,method):
    frappe.msgprint(f"New {doc.doctype} document with id {doc.name} saved successfully")