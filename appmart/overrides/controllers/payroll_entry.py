# Copyright (c) 2021, The Nexperts Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.utils import getdate, flt
import erpnext
from frappe import _
from erpnext.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry

class CustomPayrollEntry(PayrollEntry):
    def make_accrual_jv_entry(self):
        from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions
        self.check_permission("write")
        earnings = self.get_salary_component_total(component_type = "earnings") or {}
        deductions = self.get_salary_component_total(component_type = "deductions") or {}
        earnings_custom = self.get_salary_component_total(component_type = "earnings", seprate_entry = True) or {}
        deductions_custom = self.get_salary_component_total(component_type = "deductions", seprate_entry = True) or {}
        payroll_payable_account = self.payroll_payable_account
        jv_name = ""
        precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")
        if earnings or deductions:
            journal_entry = frappe.new_doc("Journal Entry")
            journal_entry.voucher_type = "Journal Entry"
            journal_entry.user_remark = _("Accrual Journal Entry for salaries from {0} to {1}")\
                .format(self.start_date, self.end_date)
            journal_entry.company = self.company
            journal_entry.posting_date = self.posting_date
            accounting_dimensions = get_accounting_dimensions() or []

            accounts = []
            currencies = []
            payable_amount = 0
            multi_currency = 0
            company_currency = erpnext.get_company_currency(self.company)

            # Earnings
            for acc_cc, amount in earnings.items():
                exchange_rate, amt = self.get_amount_and_exchange_rate_for_journal_entry(acc_cc[0], amount, company_currency, currencies)
                payable_amount += flt(amount, precision)
                accounts.append(self.update_accounting_dimensions({
                    "account": acc_cc[0],
                    "debit_in_account_currency": flt(amt, precision),
                    "exchange_rate": flt(exchange_rate),
                    "cost_center": acc_cc[1] or self.cost_center,
                    "project": self.project
                }, accounting_dimensions))

            # Deductions
            for acc_cc, amount in deductions.items():
                exchange_rate, amt = self.get_amount_and_exchange_rate_for_journal_entry(acc_cc[0], amount, company_currency, currencies)
                payable_amount -= flt(amount, precision)
                accounts.append(self.update_accounting_dimensions({
                    "account": acc_cc[0],
                    "credit_in_account_currency": flt(amt, precision),
                    "exchange_rate": flt(exchange_rate),
                    "cost_center": acc_cc[1] or self.cost_center,
                    "project": self.project
                }, accounting_dimensions))

            # Custom code for separte entry for each components start
            for acc_cc, amount in earnings_custom.items():
                exchange_rate, amt = self.get_amount_and_exchange_rate_for_journal_entry(acc_cc[0], amount, company_currency, currencies)
                #payable_amount += flt(amount, precision)
                if amount > 0:
                    accounts.append(self.update_accounting_dimensions({
                        "account": acc_cc[0],
                        "debit_in_account_currency": flt(amt, precision),
                        "exchange_rate": abs(flt(amt, precision)),
                        "cost_center": acc_cc[1] or self.cost_center,
                        "project": self.project
                    }, accounting_dimensions))
                else:
                    accounts.append(self.update_accounting_dimensions({
                        "account": acc_cc[0],
                        "credit_in_account_currency": abs(flt(amt, precision)),
                        "exchange_rate": flt(exchange_rate),
                        "cost_center": acc_cc[1] or self.cost_center,
                        "project": self.project
                    }, accounting_dimensions))

            for acc_cc, amount in deductions_custom.items():
                exchange_rate, amt = self.get_amount_and_exchange_rate_for_journal_entry(acc_cc[0], amount, company_currency, currencies)
                # payable_amount -= flt(abs(amount), precision)
                if amount > 0:
                    accounts.append(self.update_accounting_dimensions({
                        "account": acc_cc[0],
                        "credit_in_account_currency": flt(amt, precision),
                        "exchange_rate": abs(flt(amt, precision)),
                        "cost_center": acc_cc[1] or self.cost_center,
                        "project": self.project
                    }, accounting_dimensions))
                else:
                    accounts.append(self.update_accounting_dimensions({
                        "account": acc_cc[0],
                        "debit_in_account_currency": abs(flt(amt, precision)),
                        "exchange_rate": flt(exchange_rate),
                        "cost_center": acc_cc[1] or self.cost_center,
                        "project": self.project
                    }, accounting_dimensions))

            # Custom code for separte entry for each components end
            
            # Payable amount
            exchange_rate, payable_amt = self.get_amount_and_exchange_rate_for_journal_entry(payroll_payable_account, payable_amount, company_currency, currencies)
            accounts.append(self.update_accounting_dimensions({
                "account": payroll_payable_account,
                "credit_in_account_currency": flt(payable_amt, precision),
                "exchange_rate": flt(exchange_rate),
                "cost_center": self.cost_center,
                "reference_type": "Payroll Entry",
                "reference_name": self.name
                
            }, accounting_dimensions))
            print(accounts)
            journal_entry.set("accounts", accounts)
            if len(currencies) > 1:
                multi_currency = 1
            journal_entry.multi_currency = multi_currency
            journal_entry.title = payroll_payable_account
            journal_entry.save()

            try:
                journal_entry.submit()
                jv_name = journal_entry.name
                self.update_salary_slip_status(jv_name = jv_name)
            except Exception as e:
                if type(e) in (str, list, tuple):
                    frappe.msgprint(e)
                raise

        return jv_name


    def get_salary_component_total(self, component_type = None, seprate_entry = False):
        components = frappe.db.get_values("Salary Component Account",filters={"payroll_payable_account":[">","0"]},fieldname=["parent"],as_dict=True) or []
        cond = " AND 1=1 "
        if components:
            if seprate_entry :
                cond = " AND salary_component in ({}) ".format(', '.join([frappe.db.escape(i.get("parent")) for i in components]))
            else:
                cond = " AND salary_component not in ({}) ".format(', '.join([frappe.db.escape(i.get("parent")) for i in components]))
                            
        salary_components = self.get_salary_components(component_type,cond)
        if salary_components:
            component_dict = {}
            for item in salary_components:
                add_component_to_accrual_jv_entry = True
                if component_type == "earnings":
                    is_flexible_benefit, only_tax_impact = frappe.db.get_value("Salary Component", item['salary_component'], ['is_flexible_benefit', 'only_tax_impact'])
                    if is_flexible_benefit == 1 and only_tax_impact ==1:
                        add_component_to_accrual_jv_entry = False
                if add_component_to_accrual_jv_entry:
                    component_dict[(item.salary_component, item.payroll_cost_center)] \
                        = component_dict.get((item.salary_component, item.payroll_cost_center), 0) + flt(item.amount)
            if seprate_entry:
                account_details = get_account(company = self.company, component_dict = component_dict)
            else:
                account_details = self.get_account(component_dict = component_dict)
            return account_details

    def get_salary_components(self, component_type,custom_cond=" AND 1=1 "):
        salary_slips = self.get_sal_slip_list(ss_status = 1, as_dict = True)
        if salary_slips:
            salary_components = frappe.db.sql("""
                select ssd.salary_component, ssd.amount, ssd.parentfield, ss.payroll_cost_center
                from `tabSalary Slip` ss, `tabSalary Detail` ssd
                where ss.name = ssd.parent and ssd.parentfield = '%s' and ss.name in (%s) %s
            """ % (component_type, ', '.join(['%s']*len(salary_slips)),custom_cond),
                tuple([d.name for d in salary_slips]), as_dict=True,debug=True)

            return salary_components

def get_account(company, component_dict = None):
    account_dict = {}
    for key, amount in component_dict.items():
        payroll_payable_account = frappe.db.get_value("Salary Component Account", {"parent": key[0], "company": company}, "payroll_payable_account")
        account = frappe.db.get_value("Salary Component Account", {"parent": key[0], "company": company}, "account")
        if not account or not payroll_payable_account:
            frappe.throw(_("Please set account and Payroll Payable Account in Salary Component {0}").format(key[0]))
        account_dict[(account, key[1])] = account_dict.get((account, key[1]), 0) + amount
        account_dict[(payroll_payable_account, key[1])] = account_dict.get((payroll_payable_account, key[1]), 0) - amount
    return account_dict
