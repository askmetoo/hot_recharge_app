# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe import _
from frappe.model.document import Document
from hot_recharge_app.hot_recharge_app.doctype.econetbundle.econetbundle import insert_bundle
from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_api_object, get_hr_settings
from hotrecharge.HotRechargeException import HotRechargeException
from munch import munchify

class RechargeEconetBundle(Document):
	def save(self):
		bundle_rech = recharge_econet_bundle(self.bundle,self.number_to_recharge)
		
		if bundle_rech is dict:
			frappe.msgprint(
				title= 'Bundle Recharge',
				indicator= 'green',
				msg=f"Success: Econet bundle recharged to {self.number_to_recharge}!"
			)

@frappe.whitelist()
def recharge_econet_bundle(selected_bundle, number_to_recharge):
	'''
		recharge econet bundle
	'''
	try:
		api = get_hr_api_object()
		settings = get_hr_settings()

		# get selected bundle
		b = frappe.get_doc('EconetBundle', selected_bundle).as_dict()

		bundle = munchify(b)

		amount = int(bundle.amount) / 100

		resp = api.dataBundleRecharge(product_code=bundle.product_code, number=number_to_recharge, mesg=settings['bundle_customer_sms'])

		doc = frappe.new_doc('EconetBundleRecharge')
		doc.phone_number = number_to_recharge
		doc.amount = amount
		doc.data = bundle.name1
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

		new_name = f'EBR-{dt.strftime("%m-%d-%Y")}-{resp.AgentReference}'

		frappe.rename_doc('EconetBundle', doc.name, new_name)
		
		return frappe.get_doc('EconetBundle', new_name).as_dict()
		
	except HotRechargeException as hre:
		frappe.throw(_(f"Failed to buy bundle: {hre.message}"))
		return hre.message

	except Exception as err:
		frappe.throw(_(f"Failed to buy bundle: {err}"))
		return err

@frappe.whitelist()
def get_econet_bundles():
	'''
		return True if all goes well
	'''
	
	try:
		api = get_hr_api_object()

		bundles = api.getDataBundles()
		
		insert_bundle(list(bundles.Bundles))

		return True
		
	except Exception as err:
		frappe.throw(_(f"Failed to get bundles list: {err}"))
