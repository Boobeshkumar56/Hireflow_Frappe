# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TestDocument(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.Data | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Test Document"

	def before_save(self):
		if not self.description:
			self.description="Default description"
	def on_update(self):
		frappe.toast("After save called")
