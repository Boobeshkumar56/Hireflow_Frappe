# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FinanceTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		amount: DF.Currency
		employee: DF.Link | None
		expense: DF.Link | None
		status: DF.Literal["Opened", "Approved", "Rejected"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Finance Ticket"

@frappe.whitelist()
def approve_expense_ticket(finance:str):
	finance=frappe.get_doc("Finance Ticket",finance)
	expense_sheet=frappe.get_doc("Expense",finance.expense)
	expense_sheet.current_status="Processed"
	expense_sheet.finance_status="Processed"
	expense_sheet.save()
	frappe.set_value("Finance Ticket",finance.name,"status","Approved")
	frappe.msgprint("Finance ticket paid")

@frappe.whitelist()
def reject_expense_ticket(finance:str,reason:str):
	finance=frappe.get_doc("Finance Ticket",finance)
	expense_sheet=frappe.get_doc("Expense",finance.expense)
	expense_sheet.current_status="Declined"
	expense_sheet.finance_status="Failed"
	expense_sheet.finance_failure_reason=reason
	expense_sheet.save()
	frappe.set_value("Finance Ticket",finance.name,"status","Rejected")
	frappe.msgprint("Finance ticket Rejected")

