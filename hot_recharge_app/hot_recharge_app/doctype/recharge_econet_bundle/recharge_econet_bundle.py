# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from hot_recharge_app.hot_recharge_app.doctype.econetbundle.econetbundle import get_all_data, insert_bundle, get_all_data_filtered
from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_api_object

class RechargeEconetBundle(Document):
	def save(self):
		try:
			api = get_hr_api_object()

			bundle = self.bundle

			resp = api.dataBundleRecharge(product_code=bundle.ProductCode, number=self.number_to_recharge)

			# save data to db doctype
				# frappe.msgprint(
				# 	title= 'Customer Status',
				# 	indicator= 'red',
				# 	msg=f"Operation not allowed: Customer {cust_name} is blacklisted!"
				# )
			super().save()

		except Exception as err:
			print(err)
			frappe.throw(_(f"Failed to buy bundle: {err}"))

@frappe.whitelist()
def get_econet_bundles():
	try:
		# api = get_hr_api_object()

		# bundles = api.getDataBundles()
		
		# #insert_bundle( list(bundles.Bundles))

		# frappe.msgprint(
		# 			title= 'Bundles',
		# 			indicator= 'green',
		# 			msg=f"Bundles loaded!"
		# 		)

		return get_all_data_filtered()
		
	except Exception as err:
		frappe.throw(_(f"Failed to get bundles: {err}"))
