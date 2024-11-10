import frappe
from frappe import _

def configure_email():
    frappe.set_user("Administrator")
    frappe.set_value("Email Account", "Thasni", {
        "email_id": "thasni.pattathi@katara.net",
        "password": "Techi@76000#",
        "smtp_server": "10.10496.14",
        "smtp_port": 25,
        "use_ssl": 1,
        "default": 1
    })

if __name__ == "__main__":
    configure_email()

