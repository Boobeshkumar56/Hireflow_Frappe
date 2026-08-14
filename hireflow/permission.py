import frappe
from hireflow.api import get_empid
def expense_approval_query(user):
    if frappe.session.user=="Administrator":
        return ""
    employee=get_empid(user)
    if not employee:
        return "1=0"
    return f"`tabApproval`.approver = {frappe.db.escape(employee)}"

def expense_list_query(user):
    if frappe.session.user=="Administrator":
        return ""
    employee=get_empid(user)
    if not employee:
        return "1=0"
    return f"`tabExpense`.employee_id = {frappe.db.escape(employee)}"
def employee_list_query(user):
    if frappe.session.user=="Administrator":
        return ""
    employee=get_empid(user)
    if not employee:
        return "1=0"
    return f"`tabEmployee`.name = {frappe.db.escape(employee)}"
      
    
	
	