import frappe

def validate(doc, method=None):
    employees = frappe.get_all(
        "Employee",
        filters={"company": doc.company, "status": "Active"},
        fields=["name", "employee_name", "custom_tax_regime_preference"]
    )

    employee_data = []
    for emp in employees:
        salary_structure = None
        if emp.tax_regime_preference == "Old Tax Regimes":
            salary_structure = frappe.db.get_value("Salary Structure", {"regime_type": "Old Regime"}, "name")
        elif emp.tax_regime_preference == "New Tax Regimes":
            salary_structure = frappe.db.get_value("Salary Structure", {"regime_type": "New Regime"}, "name")

        if salary_structure:
            employee_data.append({
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "salary_structure": salary_structure
            })
    
    return employee_data
