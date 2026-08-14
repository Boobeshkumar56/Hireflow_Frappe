# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hireflow.api import get_receipt_data

class ExpenseList(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amount: DF.Currency
		date_of_spending: DF.Date
		description: DF.Text | None
		expense_type: DF.Literal["Commute", "Accommodation", "Food", "Others"]
		other_expense: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		receipt: DF.Attach
	# end: auto-generated types

	_DOCTYPE_NAME = "Expense List"

