# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe import _
from frappe.model.document import Document
from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_api_object, get_hr_settings
from hotrecharge.HotRechargeException import HotRechargeException
from munch import munchify

class RechargeZesa(Document):
	def save(self):
		try:
			api = get_hr_api_object()
			settings = get_hr_settings()

			# get confirmed customer
			customer = frappe.get_doc('ZesaCustomer', self.meter_number).as_dict()

			resp = api.rechargeZesa(meter_number=self.meter_number, notify_contact=self.contact_to_notify, amount=self.amount, mesg=settings['zesa_customer_sms'])

			tokens = list(resp.Tokens)

			saved_tokens = []

			for token_ in tokens:
				# save token
				doc = frappe.new_doc('ZesaToken')
				doc.customer = customer['name']
				doc.token = token_.Token
				doc.units = token_.Units
				doc.net_amount = token_.NetAmount
				doc.reference = token_.ZesaReference
				doc.insert()

				new_name = f'TOKEN-{self.meter_number}-{token_.ZesaReference}'

				frappe.rename_doc('ZesaToken', doc.name, new_name)

				saved_tokens.append(new_name)
			
			# TODO Add all tokens
			doc = frappe.new_doc('ZesaRecharge')
			doc.customer = customer['name']
			doc.account = resp.AccountName
			doc.token_sent_to = self.contact_to_notify
			doc.token = saved_tokens[0] 	# TODO Add all tokens
			doc.amount = resp.Amount
			doc.recharge_id = resp.RechargeID
			doc.reference = resp.AgentReference
			doc.reply_code = resp.ReplyCode
			doc.discount = resp.Discount
			doc.reply_sms = resp.ReplyMsg
			doc.remaining_wallet_balance = resp.WalletBalance
			doc.insert()

			dt = datetime.now()

			new_name = f'ZESA-{dt.strftime("%m-%d-%Y")}-{resp.AgentReference}'

			frappe.rename_doc('ZesaRecharge', doc.name, new_name)
		

			frappe.msgprint(
				title= 'Zesa Recharge',
				indicator= 'green',
				msg=f"Success: ZESA token sent to {self.contact_to_notify}!"
			)
			#super().save()
		
		except HotRechargeException as hre:
			print(hre)
			frappe.throw(_(f"Failed to buy zesa token: {hre.message}"))

		except Exception as err:
			print(err)
			frappe.throw(_(f"Failed to buy zesa token: {err}"))
