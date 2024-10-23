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
       
	]
    
	if filters.get('call_type') == "Incoming":
		columns.insert(1,
			{
			"label": "Date and Time",
			"fieldname": "connect1_datetime",
			"fieldtype": "datetime",
			"width": 200
		}),
		columns.insert(1,
			{
			"label": "Day",
			"fieldname": "day",
			"fieldtype": "Data",
			"width": 150
		}),
		columns.insert(3,
			{
			"label": "Called party number",
			"fieldname": "org_destination_number",
			"fieldtype": "Data",
			"width": 150
		})
		columns.insert(3,
			{
			"label": "Called From",
			"fieldname": "call_from",
			"fieldtype": "Data",
			"width": 150
		})
		columns.insert(2,
			{
			"label": "Duration",
			"fieldname": "duration",
			"fieldtype": "Duration",
			"width": 150
		})
    
	if filters.get('call_type') == "Outgoing":
		columns.insert(1,
			{
			"label": "Date and Time",
			"fieldname": "connect1_datetime",
			"fieldtype": "datetime",
			"width": 200
		}),
		columns.insert(1,
			{
			"label": "Day",
			"fieldname": "day",
			"fieldtype": "Data",
			"width": 150
		}),columns.insert(3,
			{
			"label": "Called From",
			"fieldname": "calling_party_number",
			"fieldtype": "Data",
			"width": 200
		}),
		columns.insert(3,
			{
			"label": "Call To",
			"fieldname": "call_to",
			"fieldtype": "Data",
			"width": 150
		}),columns.insert(2,
			{
			"label": "Duration",
			"fieldname": "duration",
			"fieldtype": "Duration",
			"width": 150
		})
            
	if filters.get('call_type') == "All":
		columns.insert(1,
			{
			"label": "Date and Time",
			"fieldname": "connect1_datetime",
			"fieldtype": "datetime",
			"width": 200
		}),
		columns.insert(1,
			{
			"label": "Day",
			"fieldname": "origin_day",
			"fieldtype": "Data",
			"width": 150
		}),
		columns.insert(2,
			{
			"label": "Call Type",
			"fieldname": "call_type",
			"fieldtype": "Data",
			"width": 150
		}),
		columns.insert(4,
			{
			"label": "Calling No:/Called no:",
			"fieldname": "num",
			"fieldtype": "Data",
			"width": 200
		}),
		columns.insert(4,
			{
			"label": "Call To/From",
			"fieldname": "call_number",
			"fieldtype": "Data",
			"width": 200
		}),columns.insert(3,
			{
			"label": "Duration",
			"fieldname": "duration",
			"fieldtype": "Duration",
			"width": 150
		}),
	if filters.get('call_type') == "Missed":
		columns.insert(1,
	    {
			"label": "Date and Time",
			"fieldname": "connect1_datetime",
			"fieldtype": "datetime",
			"width": 200
		}),
		columns.insert(1,
			{
			"label": "Day",
			"fieldname": "origin_day",
			"fieldtype": "Data",
			"width": 150
		}),columns.insert(3,
			{
			"label": "Missed To/Missed from",
			"fieldname": "call_number",
			"fieldtype": "Data",
			"width": 200
		}),columns.insert(2,
			{
			"label": "Duration",
			"fieldname": "duration",
			"fieldtype": "Duration",
			"width": 150
		})
            
	return columns

def get_data(filters):
	data = []
    
	if filters.get("call_type") == "Incoming":
		data = frappe.db.sql(
		"""
		SELECT 
			connect1_datetime,
			calling_party_number AS call_from,
			duration,
			Forwarded as forw_no,
			day,
			connect_time,
			org_destination_number
		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect1_date BETWEEN %s AND %s
			AND duration != '0s'
			
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
        
	if filters.get("call_type") == "Outgoing":
		data = frappe.db.sql(
		"""
		SELECT 
			connect1_datetime,
			org_destination_number AS call_to,
			duration,
			Forwarded as forw_no,
			calling_party_number,
			day
		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect1_date BETWEEN %s AND %s 
			AND duration != '0s'
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		
	if filters.get("call_type") == "All":
		incoming_data = frappe.db.sql(
		"""
		SELECT
			'Incoming' AS call_type,
			connect1_datetime,
			calling_party_number AS call_number,
			duration,
			Forwarded as forw_no,
			origin_day,
			org_destination_number as num

		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect1_date >= %s AND connect1_date <= %s
			AND duration != '0s'
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		outgoing_data = frappe.db.sql(
		"""
		SELECT
			'Outgoing' AS call_type,
			connect1_datetime,
			org_destination_number AS call_number,
			duration,
			Forwarded as forw_no,
			origin_day,
			calling_party_number as num
		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect1_date >= %s AND connect1_date <= %s
			AND duration != '0s'
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		incoming_missed= frappe.db.sql(
		"""
		SELECT
		   'Missed' AS call_type,
			connect1_datetime,
			duration,
			origin_day,
			calling_party_number AS call_number,
			org_destination_number as num
			
		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect1_date >= %s AND connect1_date <=%s
			AND duration = '0s'
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		outgoing_missed = frappe.db.sql(
		"""
		SELECT
            'Missed' AS call_type,
			connect1_datetime,
			duration,
			origin_day,
			org_destination_number AS  call_number,
		    calling_party_number as num

		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect1_date >= %s AND connect1_date <=%s
			AND duration = '0s'
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		data.extend(incoming_data)
		data.extend(outgoing_data)
		data.extend(incoming_missed)
		data.extend(outgoing_missed)

	if filters.get("call_type") == "Missed":
		incoming_missed= frappe.db.sql(
		"""
		SELECT
			connect1_datetime,
			duration,
			origin_day,
			calling_party_number AS call_number
			
		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect1_date BETWEEN %s AND %s
			AND duration = '0s'
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		outgoing_missed = frappe.db.sql(
		"""
		SELECT

			connect1_datetime,
			duration,
			origin_day,
			org_destination_number AS  call_number

		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect1_date BETWEEN %s AND %s
			AND duration = '0s'
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		data.extend(incoming_missed)
		data.extend(outgoing_missed)


	return data

def get_summary(filters, data):
    total_calls = len(data)
    total_duration = sum(item['duration'] for item in data if item.get('duration'))
    # frappe.msgprint(str(data))
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
    elif filters.get("call_type") == "Missed":
        summary = [
            {"label": "Total Missed Calls", "value": total_calls, "datatype": "Int"},
            {"label": "Total Duration", "value": total_duration, "datatype": "Duration"}
        ]
    
    
    return summary

def get_chart_data(data):
    labels = []
    durations = []

    for idx, row in enumerate(data):
        labels.append(row.get('connect1_datetime').strftime('%Y-%m-%d %H:%M') if row.get('connect1_datetime') else f"Call {idx+1}")
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