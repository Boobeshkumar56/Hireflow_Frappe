# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ExpenseLimits(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		employee: DF.Int
		lead: DF.Int
		manager: DF.Int
	# end: auto-generated types

	_DOCTYPE_NAME = "Expense Limits"
