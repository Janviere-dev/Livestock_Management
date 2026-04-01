

import frappe

def create_opening_journal_entry_after_insert(doc, method=None):
    """
    Wrapper for Frappe's after_insert event. Extracts required fields from the doc and calls create_opening_journal_entry.
    """
    # Use a valid Customer field if available, otherwise fallback to a static value
    customer = "AgriTech"  
    supplier = "Lavita Livestock ranch"
    opening_valuation_rate = getattr(doc, 'opening_valuation_rate', None)
    posting_date = getattr(doc, 'date_of_acquire', None) or frappe.utils.nowdate()
    if customer and opening_valuation_rate:
        create_opening_journal_entry(customer, supplier, opening_valuation_rate, posting_date)
    else:
        frappe.log_error(f"Missing required fields for opening journal entry: customer={customer}, opening_valuation_rate={opening_valuation_rate}", "Opening Journal Entry Error")

def create_reversing_journal_entry_on_update(doc, method=None):
    customer = "AgriTech"
    supplier = "Lavita Livestock ranch"
    closing_valuation_rate = getattr(doc, 'closing_valuation_rate', None)
    posting_date = getattr(doc, 'treatment_date', None) or getattr(doc, 'feeding_date', None) or frappe.utils.nowdate()

    if customer and closing_valuation_rate:
        create_reversing_journal_entry(customer, supplier, closing_valuation_rate, posting_date)
    else:
        frappe.log_error(f"Missing required fields for reversing journal entry: customer={customer}, closing_valuation_rate={closing_valuation_rate}", "Reversing Journal Entry Error")

@frappe.whitelist()
def create_opening_journal_entry(customer, supplier, opening_valuation_rate, posting_date=None):
    je = frappe.new_doc("Journal Entry")
    je.voucher_type = "Journal Entry"
    je.remark = "Opening Valuation Entry"
    je.posting_date = posting_date or frappe.utils.nowdate()

    # Debit Debtors (Customer)
    je.append("accounts", {
        "account": "Debtors - AFC",  
        "party_type": "Customer",
        "party": customer,
        "debit_in_account_currency": opening_valuation_rate,
        "credit_in_account_currency": 0
    })

    # Credit Creditors (Supplier)
    je.append("accounts", {
        "account": "Creditors - AFC",
        "party_type": "Supplier",
        "party": supplier,
        "debit_in_account_currency": 0,
        "credit_in_account_currency": opening_valuation_rate
    })

    je.insert()
    je.submit()
    return je.name

def create_reversing_journal_entry(customer, supplier, closing_valuation_rate, posting_date=None):
    je = frappe.new_doc("Journal Entry")
    je.voucher_type = "Journal Entry"
    je.remark = "Reversing Valuation Entry"
    je.posting_date = posting_date or frappe.utils.nowdate()

    # Debit Creditors (Supplier)
    je.append("accounts", {
        "account": "Creditors - AFC",  
        "party_type": "Supplier",
        "party": "Lavita Livestock ranch",
        "debit_in_account_currency": closing_valuation_rate,
        "credit_in_account_currency": 0
    })

    # Credit Debtors (Customer)
    je.append("accounts", {
        "account": "Debtors - AFC", 
        "party_type": "Customer",
        "party": "AgriTech",
        "debit_in_account_currency": 0,
        "credit_in_account_currency": closing_valuation_rate
    })

  

    je.insert()
    je.submit()
    return je.name