# Copyright (c) 2024, thasni and contributors
# For license information, please see license.txt



import frappe
from frappe.utils import getdate, flt

def execute(filters=None):
	agent_doc_id = filters.get("agent_id")
	agent_number = frappe.db.get_value("Call Agent", agent_doc_id, "agent_number")

	if not agent_number:
		frappe.throw("Invalid Agent Number selected")

	filters["agent_number"] = agent_number

	columns = get_columns(filters)
	data = get_data(filters)
	summary = get_summary(filters, data)
	chart = get_chart_data(data)
    
	return columns, data, None, chart, summary

def get_columns(filters):
	columns = [
		{
			"label": "Date and Time",
			"fieldname": "connect_datetime",
			"fieldtype": "datetime",
			"width": 200
		},
        {
			"label": "Duration",
			"fieldname": "duration",
			"fieldtype": "Duration",
			"width": 150
		}
	]
    
	if filters.get('call_type') == "Incoming":
		columns.insert(1,
			{
			"label": "Call From",
			"fieldname": "call_from",
			"fieldtype": "Data",
			"width": 150
		})
    
	if filters.get('call_type') == "Outgoing":
		columns.insert(1,
			{
			"label": "Call To",
			"fieldname": "call_to",
			"fieldtype": "Data",
			"width": 150
		})
            
	if filters.get('call_type') == "All":
		columns.insert(1,
			{
			"label": "Call Type",
			"fieldname": "call_type",
			"fieldtype": "Data",
			"width": 150
		}),
		columns.insert(2,
			{
			"label": "Call To/From",
			"fieldname": "call_number",
			"fieldtype": "Data",
			"width": 150
		})
            
	return columns

def get_data(filters):
	data = []
    
	if filters.get("call_type") == "Incoming":
		data = frappe.db.sql(
		"""
		SELECT 
			connect_datetime,
			calling_party_number AS call_from,
			duration,
			Forwarded as forw_no
		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect_datetime BETWEEN %s AND %s
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
        
	if filters.get("call_type") == "Outgoing":
		data = frappe.db.sql(
		"""
		SELECT 
			connect_datetime,
			org_destination_number AS call_to,
			duration,
			Forwarded as forw_no
		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect_datetime BETWEEN %s AND %s
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		
	if filters.get("call_type") == "All":
		incoming_data = frappe.db.sql(
		"""
		SELECT
			'Incoming' AS call_type,
			connect_datetime,
			calling_party_number AS call_number,
			duration,
			Forwarded as forw_no
		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect_datetime BETWEEN %s AND %s
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		outgoing_data = frappe.db.sql(
		"""
		SELECT
			'Outgoing' AS call_type,
			connect_datetime,
			org_destination_number AS call_number,
			duration,
			Forwarded as forw_no
		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect_datetime BETWEEN %s AND %s
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		data.extend(incoming_data)
		data.extend(outgoing_data)

	return data

def get_summary(filters, data):
    total_calls = len(data)
    total_duration = sum(item['duration'] for item in data if item.get('duration'))

    if filters.get("call_type") == "Incoming":
        summary = [
            {"label": "Total Incoming Calls", "value": total_calls, "datatype": "Int"},
			# {"label": "Total Transfer/Conference Calls", "value": total_forw_call, "datatype": "Duration"},
            {"label": "Total Duration", "value": total_duration, "datatype": "Duration"}
        ]
    elif filters.get("call_type") == "Outgoing":
        summary = [
            {"label": "Total Outgoing Calls", "value": total_calls, "datatype": "Int"},
            {"label": "Total Duration", "value": total_duration, "datatype": "Duration"}
        ]
    elif filters.get("call_type") == "All":
        summary = [
            {"label": "Total Calls", "value": total_calls, "datatype": "Int"},
            {"label": "Total Duration", "value": total_duration, "datatype": "Duration"}
        ]
    
    return summary

def get_chart_data(data):
    labels = []
    durations = []

    for idx, row in enumerate(data):
        labels.append(row.get('connect_datetime').strftime('%Y-%m-%d %H:%M') if row.get('connect_datetime') else f"Call {idx+1}")
        durations.append(row.get('duration', 0))
    
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Duration",
                    "values": durations
                }
            ]
        },
        "type": "bar",
        "height": 300,
        "colors": ["#FF5733"]
    }

    return chart