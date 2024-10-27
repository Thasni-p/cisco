// Copyright (c) 2024, thasni and contributors
// For license information, please see license.txt

frappe.query_reports["DATA CENTER"] = {
	"filters": [
        {
            "fieldname": "date",
            "label": __("Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.nowdate(),
            "reqd": 1
        },
        {
            "fieldname": "status",
            "label": __("status"),
            "fieldtype": "Select",
            "options": ["All", "Draft", "Rejected","Approval pending","Approved","Cancelled"],
            "default": "All"
        }
    ]
};