# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class JobPost(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		availablle: DF.Check
		no_of_openings: DF.Int
		package: DF.Float
		required_experience: DF.Int
		role: DF.Data
		skills: DF.Data
	# end: auto-generated types

	_DOCTYPE_NAME = "Job Post"
