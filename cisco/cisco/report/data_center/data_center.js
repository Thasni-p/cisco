// Copyright (c) 2024, thasni and contributors
// For license information, please see license.txt

frappe.query_reports["DATA CENTER"] = {
	"filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.nowdate(),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.nowdate(),
            "reqd": 1
        },
        {
            "fieldname": "status",
            "label": __("status"),
            "fieldtype": "Select",
            "options": ["All", "Draft", "Rejected","Pending Approval","Approved","Cancelled"],
            "default": "All"
        }
    ]
};
