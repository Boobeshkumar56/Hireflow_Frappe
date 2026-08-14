# Copyright (c) 2026, Boobesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Team(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from hireflow.hireflow.doctype.team_members.team_members import TeamMembers

		table_members: DF.Table[TeamMembers]
		team_lead: DF.Link | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Team"

	def validate(self):
		self.validate_team_members()

	def validate_team_members(self):
		employees=set()
		for row in self.table_members:
			if row.employee_id in employees:
				frappe.throw(f"Employee {row.member_name} is already in the team")
			employees.add(row.employee_id)
		existing_team=frappe.db.get_value("Team Members",{
			"employee_id":row.employee_id,
			"parenttype":"Team",
			"parent":["!=",self.name]
		})
		if existing_team:
			frappe.throw(f"Employee {row.member_name} is already in another team")