# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_api_object
from hotrecharge.HotRechargeException import HotRechargeException

class ZesaCustomer(Document):
	pass


@frappe.whitelist()
def fetch_zesa_customer(meter_number):
	try:
		# first check if customer is already saved to db
		try:
			cust = frappe.get_doc('ZesaCustomer', meter_number).as_dict()

			addr = str(cust['name1']).splitlines()

			if len(str(cust['address'])) == 0:
				cust['name1'] = addr[0]
				cust['address'] = addr[1]

			return cust

		except:
			# create customer
			pass

		api = get_hr_api_object()

		customer = api.checkZesaCustomer(meter_number)

		c_info = customer.CustomerInfo

		addr = str(c_info.CustomerName).splitlines()

		# first save contact
		doc = frappe.new_doc('ZesaCustomer')
		doc.name1 = addr[0]
		doc.address = addr[1]
		doc.meter_number = customer.Meter
		doc.reference = c_info.Reference
		doc.insert()

		frappe.rename_doc('ZesaCustomer', doc.name, customer.Meter)

		c = frappe.get_doc('ZesaCustomer', customer.Meter).as_dict()

		if len(str(c['address'])) == 0:
			c['address'] = addr[1]

		return c

	except HotRechargeException as hre:
		frappe.throw(_(f"Error: Failed to get zesa customer: {hre.message}"))
		
	except Exception as err:
		frappe.throw(_(f"Error: There was a problem getting zesa customer: {err}"))