# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_api_object
from hotrecharge.HotRechargeException import HotRechargeException

class AirtimeBalance(Document):
	pass

@frappe.whitelist()
def get_airtime_balance():
	try:
		api = get_hr_api_object()

		bal = api.walletBalance()
		
		return bal.WalletBalance
		
	except HotRechargeException as hre:
		frappe.throw(_(f"provider failed to process airtime balance: {hre.message}"))

	except Exception as err:
		frappe.throw(_(f"Failed to get Airtime balance: {err}"))