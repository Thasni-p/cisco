# Copyright (c) 2024, thasni and contributors
# For license information, please see license.txt



import frappe
from frappe.utils import getdate, flt

def execute(filters=None):

	columns = get_columns(filters)
	data = get_data(filters)
	summary = get_summary()
	chart = get_chart_data()
	
	return columns, data, None ,chart, summary

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
		},
		{

			"label": "Status",
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 150
		}
	]

	return columns

def get_data(filters):
	data = []
	
	status = filters.get("status")
	if  status == "All":
		data = frappe.db.sql(
			"""
			SELECT 
				applicant_name,
				applicant_departmentcompany,
				applicant_contact_number,
				date1,
				katara_it_managerhead_of_it_operations__name,
				workflow_state
			FROM 
				`tabData Center`
			""",
			as_dict=True
		)
	else:
		data = frappe.db.sql(
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
			WHERE 
				workflow_state = %s
				
			""",
			(filters.get("status")),
			as_dict=True
		)
		

	return data

def get_summary():
	data = frappe.db.get_all("Data Center", pluck="workflow_state")
	summary = [
		{"label": "Total Draft Requests", "value": data.count("Draft"), "datatype": "Int"}
	]
	summary += [
		{"label": "Total Rejected Request", "value": data.count("Rejected"), "datatype": "Int"}
	]
	summary += [
		{"label": "Total Pending Aprroval Request", "value": data.count("Approval pending"), "datatype": "Int"}
	]
	summary += [
		{"label": "Total Approved Request", "value": data.count("Approved"), "datatype": "Int"}
	]
	summary += [
		{"label": "Total Cancelled Request", "value": data.count("Cancelled"), "datatype": "Int"}
	]
	summary += [
		{"label": "Total Requests", "value": len(data), "datatype": "Int"}
	]
	
	return summary


from collections import Counter

def get_chart_data():
    data = frappe.db.get_all("Data Center", pluck="workflow_state")
    
    status_count = Counter(data)
    
    labels = list(status_count.keys())
    
    values = [status_count[label] for label in labels]
    
    return {
        "data": {"labels": labels, "datasets": [{"values": values}]},
        "type": "donut",
        "height": 300,
    }