# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Manager(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		data_of_joining: DF.Date | None
		department: DF.Literal["MANAGEMENT", "INFORMATION TECHNOLOGY", "SERVICE", "FINANCE", "SALES"]
		email: DF.Data | None
		employee_id: DF.Link | None
		full_name: DF.Data | None
		phone_number: DF.Phone | None
		team: DF.Data | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Manager"

	def before_insert(self):
		employee=frappe.new_doc("Employee")
		employee.employee_name=self.full_name
		employee.data_of_joining=self.data_of_joining
		employee.email=self.email
		employee.phone_number=self.phone_number
		employee.is_manager=1
		employee.department="MANAGEMENT"
		employee.insert()
		self.employee_id=employee.name
		frappe.msgprint("New employee created for manager")
		

