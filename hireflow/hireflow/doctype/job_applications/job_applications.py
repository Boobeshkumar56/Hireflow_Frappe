# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class JobApplications(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		applicant: DF.Link
		job_post: DF.Link
		verified: DF.Check
	# end: auto-generated types

	_DOCTYPE_NAME = "Job Applications"
