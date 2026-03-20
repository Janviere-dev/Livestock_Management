# Copyright (c) 2026, Janviere and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Livestock(Document):
	"""
	-In the Animal Group doctype we have: Animal Type, Breed, and Total number of animals
	- Always to register an animal we use Livestock Doctype by that animal it unique id (eg: AN###, Its animal type,
	and animal group.)
	- After we have a specific animal with Active status
	I want to automatically calculate Total animals in Animal group like
	In Animal type with this certain breed are ..., Because you have each animals unique ID
	Use freppe.db count to count those kind of animals Automatically.
	"""

	def before_save(self):
		self._previous_animal_group = None
		if not self.is_new():
			self._previous_animal_group = frappe.db.get_value("Livestock", self.name, "animal_group")

	def on_update(self):
		# Always refresh the current group count.
		self.update_animal_group_total(self.animal_group)

		# If the animal moved to another group, refresh the previous group's count too.
		previous_animal_group = getattr(self, "_previous_animal_group", None)
		if previous_animal_group and previous_animal_group != self.animal_group:
			self.update_animal_group_total(previous_animal_group)

	def on_trash(self):
		# If a livestock record is deleted, update its group's count.
		self.update_animal_group_total(self.animal_group)

	@staticmethod
	def update_animal_group_total(animal_group):
		if not animal_group or not frappe.db.exists("Animal Group", animal_group):
			return

		total_active_animals = frappe.db.count(
			"Livestock",
			filters={"animal_group": animal_group, "status": "Active"},
		)

		frappe.db.set_value(
			"Animal Group",
			animal_group,
			"total_number_of_animal",
			total_active_animals,
			update_modified=False,
		)


