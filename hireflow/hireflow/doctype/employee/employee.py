# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hireflow.api import get_empid
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum
from frappe.utils import today,get_first_day,get_last_day
class Employee(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		data_of_joining: DF.Date
		department: DF.Literal["MANAGEMENT", "INFORMATION TECHNOLOGY", "SERVICE", "FINANCE", "SALES"]
		email: DF.Data
		employee_name: DF.Data
		is_manager: DF.Check
		manager: DF.Link | None
		phone_number: DF.Data
	# end: auto-generated types

	_DOCTYPE_NAME = "Employee"

	def before_insert(self):
		...

	def has_permission(self,user=None,permission=None):
		return self.name==get_empid(frappe.session.user) or frappe.session.user=="Administrator"

	@property
	def cms(self):
		current_date = today()
		start_date = get_first_day(current_date)
		end_date = get_last_day(current_date)
		Ticket=DocType("Finance Ticket")
		month_total=(frappe.qb.from_(Ticket)
		.select(Sum(Ticket.amount).as_("Total"))
		.where((Ticket.employee==self.name ) & (Ticket.status=="Approved") & (Ticket.creation.between(start_date,end_date))))
		return month_total.run(as_list=True)[0][0] or 0

