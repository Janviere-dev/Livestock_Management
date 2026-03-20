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