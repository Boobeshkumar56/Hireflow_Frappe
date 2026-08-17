# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Approval(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action: DF.Literal["Submitted", "Accepted", "Declined", "Commented"]
		amended_from: DF.Link | None
		approver: DF.Link | None
		comment: DF.SmallText | None
		expense: DF.Link | None
		stage: DF.Literal["Team Lead", "Manager"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Approval"

	def has_permission(self,user=None):
		user=frappe.session.user
		if user ==self.owner or user=="Administrator":
			return True
		print("this is from approval")
		employee=frappe.db.get_value("Employee",{"email":user},"name")
		print(employee)
		if not employee:
			return False
		return employee==self.approver
	def on_submit(self):
		notify_user(self)



@frappe.whitelist()
def approve(approval:str):
	curr_doc=frappe.get_doc("Approval",approval)
	if curr_doc.action=="Accepted" or curr_doc.action=="Declined":
		frappe.throw("Approval is already been processed!!")
	if curr_doc.stage=="Team Lead":
		curr_doc.action="Accepted"
		curr_doc.save()
		parent_doc=frappe.get_doc("Expense",curr_doc.expense)
		parent_doc.team_lead_status="Accepted"
		parent_doc.current_status="Manager Review"
		parent_doc.save()
		manager_approval=frappe.new_doc("Approval")
		manager_approval.expense=curr_doc.expense
		manager=parent_doc.manager

		manager_approval.approver=frappe.get_value("Manager",manager,"employee_id")
		manager_approval.stage="Manager"
		manager_approval.owner=curr_doc.owner
		manager_approval.submit()
		frappe.msgprint("Approval Request Forwarded to Manager")
	else:
		curr_doc.action="Accepted"
		curr_doc.save()
		parent_doc=frappe.get_doc("Expense",curr_doc.expense)
		parent_doc.manager_status="Accepted"
		parent_doc.current_status="Finance Processing"
		parent_doc.finance_status="In Process"
		parent_doc.save()
		finance_ticket=frappe.new_doc("Finance Ticket")
		finance_ticket.employee=parent_doc.employee_id
		finance_ticket.amount=parent_doc.total_sum
		finance_ticket.expense=parent_doc.name
		finance_ticket.submit()
		frappe.msgprint("Finance Ticket Raised !!")





@frappe.whitelist()
def reject(approval:str):
	curr_doc=frappe.get_doc("Approval",approval)
	if curr_doc.action=="Accepted" or curr_doc.action=="Declined":
		frappe.throw("Approval is already been processed!!")
	curr_doc.action="Declined"
	curr_doc.save()
	parent_doc=frappe.get_doc("Expense",curr_doc.expense)
	parent_doc.team_lead_status="Declined"
	parent_doc.save()

@frappe.whitelist()
def add_comment(approval:str,comment:str):
	curr_doc=frappe.get_doc("Approval",approval)
	if curr_doc.action!="Submitted":
		frappe.throw("Approval is already been processed!!")
	curr_doc.action="Commented"
	curr_doc.save()
	parent_doc=frappe.get_doc("Expense",curr_doc.expense)
	parent_doc.team_lead_status="Commented"
	if curr_doc.stage=="Team Lead":
		parent_doc.team_lead_comment=comment
	else:
		parent_doc.manager_comment=comment
	parent_doc.save()

def notify_user(approval:Approval):
	receipent=frappe.get_value("Employee",approval.approver,"email")
	print(receipent)
	if not receipent:
		return
	frappe.get_doc({
	"doctype": "Notification Log",
    "for_user": receipent,
    "type": "Alert",
    "document_type": approval.doctype,
    "document_name": approval.name,
    "subject": f"Approval Required: {approval.name}",
    "email_content": f"""
        Approval {approval.name} requires your attention.

        Please review the expense and take the required action.
    """
	}).insert(ignore_permissions=True)

















