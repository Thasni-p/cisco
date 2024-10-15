// Copyright (c) 2024, thasni and contributors
// For license information, please see license.txt


frappe.query_reports["Call Report"] = {
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
            "fieldname": "agent_id",
            "label": __("Agent"),
            "fieldtype": "Link",
            "options": "Call Agent",
            "reqd": 1
        },
        {
            "fieldname": "call_type",
            "label": __("Call Type"),
            "fieldtype": "Select",
            "options": ["All", "Incoming", "Outgoing"],
            "default": "All"
        }
    ]
};