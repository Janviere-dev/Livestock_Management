// Copyright (c) 2026, Janviere and contributors
// For license information, please see license.txt

frappe.ui.form.on("Livestock", {

    opening_valuation_rate(frm) {
        CalculateClosingValuationRate(frm);
    },

    total_treatment_cost(frm) {
        CalculateClosingValuationRate(frm);
    },

    total_feeding_cost(frm) {
        CalculateClosingValuationRate(frm);
    },
	refresh(frm) {
		CalculateClosingValuationRate(frm);

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

        // Custom Button "Analog activity"
        
        if (!frm.is_new() && frm.doc.status === "Active"){
            frm.add_custom_button(("Log Activity"), () => {
                open_log_activity_dialog(frm)
            });
        }
	},


});

function open_log_activity_dialog(frm) {
    dialog = new frappe.ui.Dialog({
        title: "Log Activity",
        fields: [
            {
                label: "Reason for Termination",
                fieldname: "reason_for_termination",
                fieldtype: "Select",
                options: ["Sold", "Dead", "Missing", "Slaughtered"],
                reqd: 1,
                onchange: () => toggle_sold_fields(dialog),
            },

            {
                fieldtype: "Link",
                fieldname: "customer",
                label: "Customer",
                options: "Customer",
                hidden: 1,
            },

            {

                fieldtype: "Currency",
                fieldname: "selling_price",
                label: "Selling Price",
                hidden: 1,
            },

        ],
        primary_action_label:"Submit",
        primary_action(values) {
            reason = values.reason_for_termination;

            if (reason === "Sold" && (!values.customer || !values.selling_price)){
                frappe.msgprint(("Customer and Selling Price are required when reason is Sold."));
                return;

            }

            frappe.call({
            method: "livestock_management.api.create_sale_invoice", 
            args: {
                livestock_id: frm.doc.name,
                customer: values.customer,
                selling_price: values.selling_price
            },
        })

            frm.set_value("status", reason);
            frm.save();
            dialog.hide();
        },
    });
    dialog.show();
}

function toggle_sold_fields(dialog) {
    reason = dialog.get_value("reason_for_termination");
    is_sold = reason === "Sold";

    dialog.set_df_property("customer", "hidden", !is_sold);
    dialog.set_df_property("selling_price", "hidden", !is_sold);
    dialog.set_df_property("customer", "reqd", is_sold);
    dialog.set_df_property("selling_price", "reqd", is_sold);
}

function CalculateClosingValuationRate(frm) {
    // Always update closing valuation rate as the totalcost from feedings and treatment changes by adding total treatment cost, total feeding cost and opening valuation
    const opening_rate = frm.doc.opening_valuation_rate || 0;
    const total_treatment_cost = frm.doc.total_treatment_cost || 0;
    const total_feeding_cost = frm.doc.total_feeding_cost || 0;
    
    const closing_valuation_rate = opening_rate + total_treatment_cost + total_feeding_cost;
    frm.set_value('closing_valuation_rate', closing_valuation_rate);
}
