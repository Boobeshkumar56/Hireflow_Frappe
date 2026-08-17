# Copyright (c) 2026, Boobesh and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import getdate
# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


def make_employee(email,is_manager=0):
	return frappe.get_doc({
		"doctype":"Employee",
		"employee_name": email.split("@")[0],
        "email": email,
        "department": "INFORMATION TECHNOLOGY",
        "is_manager": is_manager,
		"phone_number":"9349349394",
		"data_of_joining":getdate()
    }).insert(ignore_permissions=True)
	

	
class IntegrationTestExpense(IntegrationTestCase):
	"""
	Integration tests for Expense.
	Use this class for testing interactions between multiple components.
	"""
	def setUp(self):
		self.emp=make_employee("test@hireflow.com")
	def test_total_sum_calculation(self):
		expense = frappe.get_doc({
            "doctype": "Expense",
            "employee_id": self.emp.name,
            "expenses_table": [
                {"expense_type": "Food", "date_of_spending": "2026-08-01", "amount": 1200,"receipt":"private/test"},
                {"expense_type": "Commute", "date_of_spending": "2026-08-02", "amount": 300,"receipt":"private/test"},
				
            ],
        }).insert(ignore_permissions=True)
		expense.submit()
		self.assertEqual(expense.total_sum, 1500)
	def test_throws_when_limit_exceeded(self):
		expense = frappe.get_doc({
			"doctype": "Expense",
			"employee_id": self.emp.name,
			"expenses_table": [{"expense_type": "Food", "date_of_spending": "2026-08-01", "amount": 9999,"receipt":"private/test"}],
		}).insert(ignore_permissions=True)
		self.assertRaises(frappe.ValidationError, expense.submit)