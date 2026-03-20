// Copyright (c) 2026, Janviere and contributors
// For license information, please see license.txt

frappe.ui.form.on("Treatment", {
    valuation_rate(frm) {
        calculate_total_cost(frm);
    },
    quantity(frm) {
        calculate_total_cost(frm);
    }
});

function calculate_total_cost(frm) {
    const valuation_rate = flt(frm.doc.valuation_rate) || 0;
    const quantity = flt(frm.doc.quantity) || 0;
    const total_cost = valuation_rate * quantity;
    frm.set_value("total_cost", total_cost);
}