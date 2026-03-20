// Copyright (c) 2026, Janviere and contributors
// For license information, please see license.txt

frappe.ui.form.on("Livestock", {
	refresh(frm) {
        frm.set_query("breed", function(){
            return{

                filters:{animal_type: frm.doc.animal_type}
            }
        })
        frm.set_query("animal_group", function(){
            return{

                filters:{breed: frm.doc.breed}
            }
        })



	},
});
