import frappe
from frappe.model.document import Document
from datetime import date, datetime

class Transaction(Document):

	def validate(self):
		book = frappe.get_doc("Book", self.book)
		member = frappe.get_doc("Member", self.member)
		
		if self.status == "Issued":
			# Book availability check
			if book.available_qty <= 0:
				frappe.throw("Book is not available in stock.")

			# Member debt limit check
			if member.outstanding_debt >= 500:
				frappe.throw("Member has exceeded the Rs. 500 debt limit.")

		elif self.status == "Returned":
			# Set return_date to today if not provided
			if not self.return_date:
				self.return_date = date.today()

			# Parse dates properly
			issue_date = self.issue_date
			
			return_date = self.return_date
			
			# Ensure both dates are date objects
			if isinstance(issue_date, str):
				issue_date = datetime.strptime(issue_date, "%Y-%m-%d").date()
			if isinstance(return_date, str):
				return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

			# Calculate number of days (at least 1)
			days = (return_date - issue_date).days
			days = max(1, days)

			# Calculate rent fee and assign
			rent_fee = 5 * days
			self.rent_fee = rent_fee

			# Update member debt
			member.outstanding_debt += rent_fee
			frappe.db.set_value("Member", self.member, "outstanding_debt", member.outstanding_debt)

	def on_submit(self):
		book = frappe.get_doc("Book", self.book)

		if self.status == "Issued":
			book.available_qty -= 1

		elif self.status == "Returned":
			book.available_qty += 1

		book.save()
