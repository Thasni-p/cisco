# Copyright (c) 2024, thasni and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return get_columns(),


def get_columns():
	values_field_type = "Data"  # TODO: better text wrapping in reportview
	columns = [
		{"label": "Number", "fieldname": "destination_number", "fieldtype": "Data", "width": 200},
		{"label": "Device Name", "fieldname": "destination_device_name", "fieldtype": "Data", "width": 500},
		{"label": "Duration of Call", "fieldname": "duration", "fieldtype": "int", "width": 200},
		{"label": "Date Time Connect", "fieldname": "date_time_connect", "fieldtype": "Datetime", "width": 200},
		{"label": "Date Time Disconnect", "fieldname": "date_time_disconnect", "fieldtype": "Datetime", "width": 200},
		# {"label": "Devide Ip Address", "fieldname": "device_ip", "fieldtype": "Data", "width": 200},
		{"label": "Call Behaviour", "fieldname": "destination_cause_value", "fieldtype": "Data", "width": 200},
	]

	# Each app is shown in order as a column
	installed_apps = frappe.get_installed_apps(_ensure_on_bench=True)
	columns += [{"label": app, "fieldname": app, "fieldtype": values_field_type} for app in installed_apps]

	return columns




