# Copyright (c) 2024, thasni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import csv
from io import StringIO
import requests
from frappe.utils import get_url, convert_utc_to_system_timezone, get_system_timezone,get_weekday,getdate
from datetime import datetime, timezone
import pytz


class CDRUpload(Document):
	pass


@frappe.whitelist()
def process_cdr(doc_id):
	# Get system timezone
	system_timezone_str = get_system_timezone()
	system_timezone = pytz.timezone(system_timezone_str)

	# Get doc
	cdr_doc = frappe.get_doc('CDR Upload', doc_id)
	url = cdr_doc.file_attach
    
	# Get full url of the attachment file
	csv_url = f"{get_url()}{url}"
    
	# Process and read the csv file
	response = requests.get(csv_url)
	# response.raise_for_status()

	csv_data = StringIO(response.text)
	reader = csv.DictReader(csv_data)

	headers = next(reader)  # Read the header row
	next(reader)  # Skip the second row

	dict_reader = csv.DictReader(csv_data, fieldnames=headers)

	for row in dict_reader:
			connect_timestamp = int(row['dateTimeConnect'])
			connect_utc_datetime = datetime.fromtimestamp(connect_timestamp, tz=timezone.utc)
			connect_date_time_origin = connect_utc_datetime.astimezone(system_timezone).replace(tzinfo=None)

			connect1_timestamp = int(row['dateTimeOrigination'])
			connect1_utc_datetime = datetime.fromtimestamp(connect1_timestamp, tz=timezone.utc)
			connect1_date_time_origin = connect1_utc_datetime.astimezone(system_timezone).replace(tzinfo=None)


			disconnect_timestamp = int(row['dateTimeDisconnect'])
			disconnect_utc_datetime = datetime.fromtimestamp(disconnect_timestamp, tz=timezone.utc)
			disconnect_date_time_origin = disconnect_utc_datetime.astimezone(system_timezone).replace(tzinfo=None)
		
			forward = 0
			if not row['originalCalledPartyNumber'] == row['finalCalledPartyNumber']:
				forward = 1
			# if(row['dateTimeConnect'] and int(row['dateTimeConnect'])>0 and type(row['dateTimeDisconnect']=='str'))
			doc = frappe.get_doc({
				'doctype': 'Call Summary',
				'cdr_id': doc_id,
				# 'call_id': row['globalCallID_callId'],
				'calling_party_number': row['callingPartyNumber'],
				'org_destination_number': row['originalCalledPartyNumber'],
				'final_destination_number': row['finalCalledPartyNumber'],
				'forwarded': forward,
				'day': get_weekday(getdate(connect_date_time_origin.date())),
				'origin_day': get_weekday(getdate(connect1_date_time_origin.date())),
				'connect1_datetime': connect1_date_time_origin ,
				'connect_datetime': connect_date_time_origin,
				'disconnect_datetime': disconnect_date_time_origin,
				'connect_date': connect_date_time_origin.date(),
				'connect_time': connect_date_time_origin.time(),
				'connect1_date': connect1_date_time_origin.date(),
				'connect1_time': connect1_date_time_origin.time(),
				'disconnect_date': disconnect_date_time_origin.date(),
				'disconnect_time': disconnect_date_time_origin.time(),
				'duration': row['duration'],
				'origin_device_name': row['origDeviceName'],
				'destination_device_name': row['destDeviceName']

			})
			doc.insert(ignore_permissions=True)		
        
	frappe.db.commit()
	frappe.msgprint("Data successfully imported.")