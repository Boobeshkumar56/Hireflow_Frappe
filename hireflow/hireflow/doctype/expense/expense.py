# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum

from hireflow.api import process_expense


class Expense(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from hireflow.hireflow.doctype.expense_list.expense_list import ExpenseList

		amended_from: DF.Link | None
		current_status: DF.Literal["Team Lead Review", "Manager Review", "Finance Processing", "Processed", "Declined"]
		department: DF.Data | None
		employee_id: DF.Link | None
		expenses_table: DF.Table[ExpenseList]
		finance_failure_reason: DF.SmallText | None
		finance_status: DF.Literal["Pending", "In Process", "Failed", "Processed"]
		manager: DF.Data | None
		manager_comment: DF.SmallText | None
		manager_status: DF.Literal["Pending", "Accepted", "Declined", "Commented"]
		name1: DF.Data | None
		team_lead: DF.Link | None
		team_lead_comment: DF.SmallText | None
		team_lead_status: DF.Literal["Pending", "Accepted", "Declined", "Commented"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Expense"

	def before_submit(self):
		expense_list=DocType("Expense List")
		sum=frappe.qb.from_(expense_list).select(Sum(expense_list.amount)).where(expense_list.parent==self.name)
		self.total_sum=sum.run(as_list=True)[0][0] or 0
		curr_user=frappe.get_doc("Employee",self.employee_id)
		user_type="manager" if curr_user.is_manager else "lead" if frappe.db.exists("Team Lead",{"lead_id":self.employee_id}) else "employee"
		allowed_expense_limit=frappe.get_single_value("Expense Limits",user_type)
		if allowed_expense_limit is None:
			frappe.throw(f"No expense limit configured for '{user_type}'. Contact Admin to set it up.")
		if curr_user.cms+self.total_sum>allowed_expense_limit :
			frappe.throw("Expenses Montly Limit Exceeding")



	def on_submit(self):
		# Enqueue background job to process the expense after commit
		frappe.enqueue(method="hireflow.api.process_expense", expense_name=self.name, queue="long", enqueue_after_commit=True)
		


	def has_permission(self,user=None):
			user=frappe.session.user
			if user ==self.owner or user=="Administrator":
				return True
			employee=frappe.db.get_value("Employee",{"email":user},"name")
			if not employee:
				return False
			manager_emp=frappe.get_value("Manager",self.manager,"employee_id") if self.manager else None
			return employee==self.team_lead or employee==manager_emp
