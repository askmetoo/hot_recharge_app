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
		try:
			api = get_hr_api_object()
			settings = get_hr_settings()

			resp = api.rechargePinless(amount=self.amount, number=self.phone_number, mesg=settings['airtime_customer_sms'])

			doc = frappe.new_doc('RechargeAirtime')
			doc.phone_number = self.phone_number
			doc.amount = self.amount
			doc.initial_balance = resp.InitialBalance
			doc.final_balance = resp.FinalBalance
			doc.recharge_id = resp.RechargeID
			doc.reference = resp.AgentReference
			doc.reply_code = resp.ReplyCode
			doc.discount = resp.Discount
			doc.reply_sms = resp.ReplyMsg
			doc.remaining_wallet_balance = resp.WalletBalance
			doc.insert()

			dt = datetime.datetime.now()

			new_name = f'ART-{dt.strftime("%m-%d-%Y")}-{resp.AgentReference}'

			frappe.rename_doc('RechargeAirtime', doc.name, new_name)
			doc.reload()

			frappe.msgprint(
				title= 'Airtime Recharge',
				indicator= 'green',
				msg=f"Success: Airtime recharged to {self.phone_number}!"
			)
			#super().save()
		
		except HotRechargeException as hre:
			print(hre)
			frappe.throw(_(f"Failed to buy airtime: {hre.message}"))

		except Exception as err:
			print(err)
			frappe.throw(_(f"Failed to buy airtime: {err}"))
