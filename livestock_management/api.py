import frappe

@frappe.whitelist()
def create_sale_invoice(livestock_id, customer, selling_price):
    sales_invoice = frappe.new_doc("Sales Invoice")
    sales_invoice.customer = customer
    sales_invoice.custom_livestock_id = livestock_id
    sales_invoice.custom_selling_price = selling_price
   
    sales_invoice.append("items", {
        "item_code": "FEED-001",
        "qty": 1,
    })

    sales_invoice.insert()
    sales_invoice.submit()
    
    return sales_invoice.name
