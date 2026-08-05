# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Employee(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		department: DF.Literal["SD", "TEST", "HR", "TL", "MGR"]
		dob: DF.Date
		email: DF.Data
		employee_name: DF.Data
		phone_number: DF.Data
	# end: auto-generated types

	_DOCTYPE_NAME = "Employee"

	def before_insert(self):
		try:
			if frappe.db.exists("User", {"email": self.email}):
				frappe.throw("A User already exists for this email.")

			user = frappe.new_doc("User")
			user.first_name = self.employee_name
			user.email = self.email
			user.user_type = "System User"

			user.append("roles", {
				"role": self.department
			})

			user.insert(ignore_permissions=True)
			
			frappe.msgprint("User Created Successfully")

		except Exception:
			frappe.throw(frappe.get_traceback())

def has_permission(doc,user=None):
	if not user:
		user = frappe.session.user

	if user == "Administrator":
		return None
	
	if "HR" in frappe.get_roles(user):
		return True
	
	return doc.email == user


def get_permission_query_conditions(user):
	if not user:
		user = frappe.session.user

	if user == "Administrator":
		return None
	
	if "HR" in frappe.get_roles(user):
		return None
	
	if not "HR" in frappe.get_roles(user):
		return f"`tabEmployee`.email = {frappe.db.escape(user)}"
