# Copyright (c) 2021, The Nexperts Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.utils import flt


def before_save(doc,method):
    if False and doc.get("base") and doc.get("employee_salary_components"):
        total_amount = flt(0)
        for comp in doc.get("employee_salary_components"):
            if comp.get("type") == "Earning":
                total_amount += comp.get("amount") or 0
        if total_amount > doc.get("base"):
            frappe.throw("<b> Salary Components </b> total cannot be greater than <b> Base </b>")

@frappe.whitelist()
def get_components(doctype='Salary Structure Assignment', txt='', searchfield='name', start=0, page_len=20, filters=None, as_dict=False):
    return frappe.db.get_values("Salary Detail",filters={"parent":filters.get("salary_structure")},fieldname=["salary_component"]) or []
