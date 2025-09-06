import frappe
from frappe.utils import add_days, formatdate, nowdate
import frappe
from frappe.utils import add_days, formatdate, nowdate

def validate(self, method=None):
    # Probation -> Final Confirmation Date logic
    if self.date_of_joining and self.custom_probation_days:
        probation_days = int(self.custom_probation_days)
        final_confirmation_date = add_days(self.date_of_joining, probation_days)
        self.final_confirmation_date = final_confirmation_date

        # Agar probation complete ho gaya toh status Active
        if final_confirmation_date <= nowdate() and self.status not in ["Left", "Inactive"]:
            self.status = "Active"

        frappe.msgprint(
            f"Final Confirmation Date: {formatdate(final_confirmation_date)} | Status set to {self.status}"
        )

    # Resignation -> Notice Period -> Last Working Date logic
    if self.resignation_letter_date and self.notice_number_of_days:
        notice_days = int(self.notice_number_of_days)
        relieving_date = add_days(self.resignation_letter_date, notice_days)

        # Field set karna
        self.relieving_date = relieving_date

        # Agar relieving_date aagaya toh status ko Left karna
        if self.relieving_date:
            self.status = "Left"

        frappe.msgprint(
            f"Last Working Date (after Notice Period): {formatdate(relieving_date)} | Status set to {self.status}"
        )

