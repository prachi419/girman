# Copyright (c) 2025, Orachi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EmployeeInvestmentDeclaration(Document):
	pass

	import frappe

	def validate(self, method=None):
		
		inv = frappe.get_value(
			"Employee Investment Declaration",
			{"employee": self.employee, "financial_year": self.financial_year},
			["section_80c", "section_80d", "other_exemption"],
			as_dict=True
		)

		if inv:
			total_exemptions = (inv.section_80c or 0) + (inv.section_80d or 0) + (inv.other_exemption or 0)
			self.total_investment_declared = total_exemptions
