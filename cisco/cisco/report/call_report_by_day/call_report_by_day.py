# Copyright (c) 2024, thasni and contributors
# For license information, please see license.txt

# import frappe



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
			"label": "Date",
			"fieldname": "connect1_date",
			"fieldtype": "date",
			"width": 200
		},
		 {
			"label": "Duration",
			"fieldname": "dur",
			"fieldtype": "Duration",
			"width": 150
		}
	]
    
	if filters.get('call_type') == "Incoming":
		columns.insert(1,
			{
			"label": "Day",
			"fieldname": "origin_day",
			"fieldtype": "Data",
			"width": 150
		}),columns.insert(3,
		{
			"label": "Number of Calls",
			"fieldname": "no_calls",
			"fieldtype": "Data",
			"width": 150
		})
    
	if filters.get('call_type') == "Outgoing":
		columns.insert(1,
			{
			"label": "Day",
			"fieldname": "origin_day",
			"fieldtype": "Data",
			"width": 150
		}),columns.insert(2,
		{
			"label": "Number of Calls",
			"fieldname": "no_calls",
			"fieldtype": "Data",
			"width": 150
		})
	if filters.get('call_type') == "Missed":
		columns.insert(1,
			{
			"label": "Day",
			"fieldname": "origin_day",
			"fieldtype": "Data",
			"width": 150
		}),columns.insert(2,
		{
			"label": "Number of Calls",
			"fieldname": "no_calls",
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
		}),columns.insert(2,
		{
			"label": "Day",
			"fieldname": "origin_day",
			"fieldtype": "Data",
			"width": 150
		}),columns.insert(3,
		{
			"label": "Number of Calls",
			"fieldname": "no_calls",
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
			count(calling_party_number) as no_calls,
			sum(duration) as dur,
			Forwarded,
			origin_device_name,
			connect1_date,
			destination_device_name,
			origin_day
		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect1_date BETWEEN %s AND %s
			group by origin_day
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
			count(org_destination_number) as no_calls,
			sum(duration) as dur,
			Forwarded,
			connect1_date,
			origin_device_name,
			destination_device_name,
			origin_day
		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect1_date BETWEEN %s AND %s
			group by origin_day
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
			count(calling_party_number) as no_calls,
			sum(duration) as dur,
			Forwarded,
			connect1_date,
			origin_device_name,
			destination_device_name,
			origin_day
		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect1_date BETWEEN %s AND %s
			group by origin_day
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
			count(org_destination_number) as no_calls,
			sum(duration) as dur,
			Forwarded,
			connect1_date,
			origin_device_name,
			destination_device_name,
			origin_day
		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect1_date BETWEEN %s AND %s
			group by origin_day
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		incoming_missed= frappe.db.sql(
		"""
		SELECT
		   'Incoming Missed' AS call_type,
			connect1_datetime,
			duration,
			origin_day,
			connect1_date,
			calling_party_number AS call_number,
			count(calling_party_number) AS no_calls

		FROM 
			`tabCall Summary`
		WHERE 
			org_destination_number = %s
			AND connect1_date BETWEEN %s AND %s
			AND duration = '0s'
			group by origin_day
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		outgoing_missed = frappe.db.sql(
		"""
		SELECT
            'Outgoing Missed' AS call_type,
			connect1_datetime,
			duration,
			origin_day,
			connect1_date,
			org_destination_number AS  call_number,
			count(org_destination_number) as no_calls

		FROM 
			`tabCall Summary`
		WHERE 
			calling_party_number = %s
			AND connect1_date BETWEEN %s AND %s
			AND duration = '0s'
			group by origin_day
		
		""",
		(filters.get("agent_number"), filters.get("from_date"), filters.get("to_date")),
		as_dict=True
	)
		data.extend(incoming_data)
		data.extend(outgoing_data)
		data.extend(incoming_missed)
		data.extend(outgoing_missed)
	return data

def get_summary(filters, data):
    total_calls = sum(item['no_calls'] for item in data if item.get('no_calls'))
    total_duration = sum(item['dur'] for item in data if item.get('dur'))

    if filters.get("call_type") == "Incoming":
        summary = [
            {"label": "Total Incoming Calls", "value": total_calls, "datatype": "Int"},
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
    callnumbers = []

    for idx, row in enumerate(data):
        labels.append(row.get('origin_day') if row.get('origin_day') else f"Call {idx+1}")
        callnumbers.append(row.get('no_calls', 0))
    
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Number of Calls",
                    "values": callnumbers
                }
            ]
        },
        "type": "bar",
        "height": 300,
        "colors": ["#FF5733"]
    }

    return chart
