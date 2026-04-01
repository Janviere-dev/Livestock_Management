# Copyright (c) 2026, Janviere and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LivestockRecordAudit(Document):
	pass

def create_livestock_audit(doc, method=None):
	"""
	Creates a historical record in 'Livestock Record Audit' 
	whenever a change happens to livestock.
	"""
	
	
	audit_doc = frappe.new_doc("Livestock Record Audit")
	
	audit_doc.livestock_id = doc.name           
	audit_doc.valuation_rate = doc.closing_valuation_rate
	audit_doc.activity = doc.status
	audit_doc.insert(ignore_permissions=True)
	audit_doc.submit()