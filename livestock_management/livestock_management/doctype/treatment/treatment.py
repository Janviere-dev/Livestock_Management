# Copyright (c) 2026, Janviere and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class Treatment(Document):
    
    def on_submit(self):
        self.apply_treatment_cost(delta_sign=1)

    def on_cancel(self):
        self.apply_treatment_cost(delta_sign=-1)

    def apply_treatment_cost(self, delta_sign=1):
        total_cost = flt(self.total_cost)
        is_submit = (delta_sign == 1)

        if self.entry_type == "Individual" and self.animal_id:
            self._update_livestock_history_and_total(self.animal_id, delta_sign * total_cost, is_submit)
            return

        if self.entry_type == "Group" and self.group_id:
            livestock_list = frappe.get_all(
                "Livestock",
                filters={"animal_group": self.group_id, "status": "Active"},
                pluck="name",
            )

            count = len(livestock_list)
            if count > 0:
                cost_per_animal = total_cost / count
                delta = delta_sign * cost_per_animal

                for livestock_name in livestock_list:
                    self._update_livestock_history_and_total(livestock_name, delta, is_submit)

    


    def _update_livestock_history_and_total(self, livestock_name, cost_delta, is_submit=True):
        # 1. Load the full Livestock document
        livestock_doc = frappe.get_doc("Livestock", livestock_name)

        # 2. Update the Total Treatment Cost field
        current_total = flt(livestock_doc.total_treatment_cost)
        livestock_doc.total_treatment_cost = max(0, current_total + flt(cost_delta))

         # avoid negative on cancel edge-cases
        if livestock_doc.total_treatment_cost < 0:
            livestock_doc.total_treatment_cost = 0


        # 3. Handle the Child Table Row
        if is_submit:
            # Add a new row to the history log on Submit
            new_row = livestock_doc.append("livestock_treatment_log", {})
            new_row.treatment_id = self.name
            new_row.treatment_date = self.treatment_date
            new_row.product= self.product
            new_row.quantity= self.quantity
            # new_row.total_cost= self.total_cost

            # We store the specific cost share (individual or split)
            new_row.total_cost = abs(cost_delta) 
        else:
            # Remove the row if the treatment is Cancelled
            # We find the row that matches this treatment's ID and remove it
            livestock_doc.set("livestock_treatment_log", [
                row for row in livestock_doc.livestock_treatment_log 
                if row.treatment_id != self.name
            ])

        
        # Calculate and update closing valuation rate before saving
        opening_rate = livestock_doc.opening_valuation_rate or 0
        total_treatment_cost = livestock_doc.total_treatment_cost or 0
        total_feeding_cost = livestock_doc.total_feeding_cost or 0
        closing_valuation_rate = opening_rate + total_treatment_cost + total_feeding_cost
        livestock_doc.closing_valuation_rate = closing_valuation_rate
        
        # 4. Save the changes (after all updates, including closing valuation)
        livestock_doc.save(ignore_permissions=True)


    



       