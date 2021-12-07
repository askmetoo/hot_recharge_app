# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_api_object, get_hr_settings

class QuickAirtimeRecharge(Document):
	pass

	def recharge(self):
		'''
			perform airtime 
		'''
		api = get_hr_api_object()

		configs = get_hr_settings()

		if api:
			# recharge
			response = api.rechargePinless(amount=amount, number=cleaned_number, mesg=configs.get('airtime_customer_sms'))
            
			pass

		else:
			# show pop
			pass