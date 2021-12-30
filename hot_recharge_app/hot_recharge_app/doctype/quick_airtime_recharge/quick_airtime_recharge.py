# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt


import datetime
import frappe
from frappe import _
from frappe.model.document import Document
from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_api_object, get_hr_settings
from hotrecharge.HotRechargeException import HotRechargeException

class QuickAirtimeRecharge(Document):
	def save(self):
		recharge = quick_recharge(amount=self.amount, phone_number=self.phone_number)

		if recharge is dict:
			frappe.msgprint(
			title= 'Airtime Recharge',
			indicator= 'green',
			msg=f"Success: Airtime recharged to {self.phone_number}!"
		)

@frappe.whitelist()
def quick_recharge(amount, phone_number):
	'''
		perform a quick airtime recharge
		returns the saved doc as a dict
	'''
	try:
		api = get_hr_api_object()
		settings = get_hr_settings()

		resp = api.rechargePinless(amount=amount, number=phone_number, mesg=settings['airtime_customer_sms'])

		doc = frappe.new_doc('RechargeAirtime')
		doc.phone_number = phone_number
		doc.amount = amount
		doc.initial_balance = resp.InitialBalance
		doc.final_balance = resp.FinalBalance
		doc.recharge_id = resp.RechargeID
		doc.reference = resp.AgentReference
		doc.reply_code = resp.ReplyCode
		doc.discount = resp.Discount
		doc.reply_sms = resp.ReplyMsg
		doc.remaining_wallet_balance = resp.WalletBalance
		doc.insert()
		# doc.reload()

		dt = datetime.datetime.now()

		new_name = f'ART-{dt.strftime("%m-%d-%Y")}-{resp.AgentReference}'

		frappe.rename_doc('RechargeAirtime', doc.name, new_name)
		#doc.reload()

		return frappe.get_doc('RechargeAirtime', new_name).as_dict()

	except HotRechargeException as hre:
		frappe.throw(_(f"Failed to buy airtime: {hre.message}"))
		return hre.message

	except Exception as err:
		frappe.throw(_(f"Failed to buy airtime: {err}"))
		return err