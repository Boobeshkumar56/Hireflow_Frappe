# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Applicant(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		contact: DF.Data
		dob: DF.Date
		education: DF.Literal["B.E.", "B.Tech", "Others"]
		email: DF.Data
		name1: DF.Data
		resume: DF.Attach
	# end: auto-generated types

	_DOCTYPE_NAME = "Applicant"
