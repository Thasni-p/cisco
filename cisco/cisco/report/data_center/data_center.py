# Copyright (c) 2024, thasni and contributors
# For license information, please see license.txt



import frappe
from frappe.utils import getdate, flt

def execute(filters=None):

	columns = get_columns(filters)
	data = get_data(filters)
	summary = get_summary(filters, data)
	chart = get_chart_data(data)
    
	return columns, data, None, chart, summary

def get_columns(filters):
	columns = [
        {
			"label": "Applicant Name",
			"fieldname": "applicant_name",
			"fieldtype": "data",
			"width": 200
		},
		{
			"label": "Applicant Department/Company",
			"fieldname": "applicant_departmentcompany",
			"fieldtype": "data",
			"width": 250
		},
		 {
			"label": "Applicant Contact Number",
			"fieldname": "applicant_contact_number",
			"fieldtype": "Phone",
			"width": 200
		},
		{
			"label": "Date",
			"fieldname": "date1",
			"fieldtype": "datetime",
			"width": 200
		},
		{
			"label": "Approved By",
			"fieldname": "katara_it_managerhead_of_it_operations__name",
			"fieldtype": "data",
			"width": 200
		}
	]
	if filters.get('status') == "All":
		columns.insert(0,
			{
			"label": "status",
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 150
		})

	return columns

def get_data(filters):
	data = []
    
	if filters.get("status") == "Draft":
		data = frappe.db.sql(
		"""
		SELECT 
			applicant_name,
			applicant_departmentcompany,
			applicant_contact_number,
			date1,
			katara_it_managerhead_of_it_operations__name
		FROM 
			`tabData Center`
		WHERE 
			workflow_state = %s
			
		""",
		(filters.get("status")),
		as_dict=True
	)
	if filters.get("status") == "Rejected":
		data = frappe.db.sql(
		"""
		SELECT 
			applicant_name,
			applicant_departmentcompany,
			applicant_contact_number,
			date1,
			katara_it_managerhead_of_it_operations__name
		FROM 
			`tabData Center`
		WHERE 
			workflow_state = %s
			
		""",
		(filters.get("status")),
		as_dict=True
	)
	if filters.get("status") == "Approval pending":
		data = frappe.db.sql(
		"""
		SELECT 
			applicant_name,
			applicant_departmentcompany,
			applicant_contact_number,
			date1,
			katara_it_managerhead_of_it_operations__name
		FROM 
			`tabData Center`
		WHERE 
			workflow_state = %s
			
		""",
		(filters.get("status")),
		as_dict=True
	)
	if filters.get("status") == "Approved":
		data = frappe.db.sql(
		"""
		SELECT 
			applicant_name,
			applicant_departmentcompany,
			applicant_contact_number,
			date1,
			katara_it_managerhead_of_it_operations__name
		FROM 
			`tabData Center`
		WHERE 
			workflow_state = %s
			
		""",
		(filters.get("status")),
		as_dict=True
	)
	if filters.get("status") == "Cancelled":
		data = frappe.db.sql(
		"""
		SELECT 
			applicant_name,
			applicant_departmentcompany,
			applicant_contact_number,
			date1,
			katara_it_managerhead_of_it_operations__name
		FROM 
			`tabData Center`
		WHERE 
			workflow_state = %s
			
		""",
		(filters.get("status")),
		as_dict=True
	)
	if filters.get("status") == "All":
		data1 = frappe.db.sql(
	    """
		SELECT 
		    workflow_state  AS status,
			applicant_name,
			applicant_departmentcompany,
			applicant_contact_number,
			date1,
			katara_it_managerhead_of_it_operations__name
		FROM 
			`tabData Center`
		
			
		""",
		
	)
		data.extend(data1)
		

	return data

def get_summary(filters, data):
    total_status = len(data)
    if filters.get("status") == "Draft":
        summary = [
            {"label": "Total Draft Requests", "value": total_status, "datatype": "Int"}
        ]
    elif filters.get("status") == "Rejected":
        summary = [
            {"label": "Total Rejected Request", "value": total_status, "datatype": "Int"}
        ]
    elif filters.get("status") == "Approval pending":
        summary = [
            {"label": "Total Pending Aprroval Request", "value": total_status, "datatype": "Int"}
        ]
    elif filters.get("status") == "Approved":
        summary = [
            {"label": "Total Approved Request", "value": total_status, "datatype": "Int"}
        ]
    elif filters.get("status") == "Cancelled":
        summary = [
            {"label": "Total Cancelled Request", "value": total_status, "datatype": "Int"}
        ]
    elif filters.get("status") == "All":
        summary = [
            {"label": "Total Requests", "value": total_status, "datatype": "Int"}
        ]
    
    return summary
def get_chart_data(data):
    labels = []
    durations = []

    for idx, row in enumerate(data):
        labels.append(row.get('date1').strftime('%Y-%m-%d ') )
        durations.append(row.get('workflow_state', 0))
    
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "workflow_state",
                    "values": durations
                }
            ]
        },
        "type": "pie",
        "height": 300,
        "colors": ["#FF5733"]
    }

    return chart


