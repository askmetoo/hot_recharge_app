# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_api_object, get_hr_settings
from hotrecharge.HotRechargeException import HotRechargeException

class RechargeAirtime(Document):
	pass

@frappe.whitelist()
def query(reference):
	'''
		query a transaction
	'''
	try:
		api = get_hr_api_object()

		resp = api.queryTransactionReference(reference)

		return resp.RawReply

	except HotRechargeException as hre:
		return hre.message

	except Exception as err:
		print(err)
		frappe.throw(_(f"Failed to query transaction: {err}"))


