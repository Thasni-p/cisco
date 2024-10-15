import frappe
from frappe import _
# import json
import frappe
from frappe import _
from frappe.utils.file_manager import save_file
from frappe.utils import today

@frappe.whitelist(allow_guest=True)
def upload_cdr_file_csv(fname, csv_file):
	try:
		if not csv_file:
			return {"status": "error", "message": "CSV File Mandatory"}
		csv_doc = frappe.get_doc({
			"doctype": "CDR Upload",
			"from_date": today(),
			"to_date": today(),
		})
		csv_doc.flags.ignore_mandatory = True
		csv_doc.insert(ignore_permissions=True)
		
		# Step 2: Attach the CSV file
		# Decode the file content (csv_file should be base64 encoded)
		file_data = frappe.safe_decode(csv_file)
		# file_name = "csvfile.csv"
		saved_file = save_file(fname, file_data, "CDR Upload", csv_doc.name, decode=True, is_private=True, df="file_attach")
		
		# Set the file URL in a custom field'
		csv_doc.file_attach = saved_file.file_url
		csv_doc.save()
		
		frappe.db.commit()
		return {"status": "success", "message": _("CDR Uploaded successfully"), "cdr_ref": csv_doc.name}
	
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), _("CDR Upload Creation Failed"))
		return {"status": "error", "message": str(e)}
