# Copyright (c) 2026, Janviere and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AnimalGroup(Document):
	def validate(self):
		self.total_number_of_animal = frappe.db.count(
			"Livestock",
			filters={"animal_group": self.name, "status": "Active"},
		)
