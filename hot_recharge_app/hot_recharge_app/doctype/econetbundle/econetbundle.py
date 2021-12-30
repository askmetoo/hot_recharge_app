# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from hot_recharge_app.hot_recharge_app.hr_api_object import get_hr_settings

class EconetBundle(Document):
	pass


@frappe.whitelist()
def insert_bundle(bundles: list):

	'''
	categories: Network

	Econet Data
	Econet Text
	Econet Twitter
	Econet Instagram
	Econet Facebook
	Econet WhatsApp
	'''

	# remove previously added data
	delete_all_data()

	# check if conversion is set
	settings = get_hr_settings()

	convert = settings.get('use_conversion', False)
	rate = settings.get('conversion_rate', 1)
	curr = settings.get('currency', 'ZAR')
	
	for bundle in bundles:
		try:
			doc = frappe.new_doc('EconetBundle')
			doc.name1 = bundle.Name
			doc.product_code = bundle.ProductCode
			doc.amount= bundle.Amount
			doc.validity_period=bundle.ValidityPeriod
			doc.bundle_id = bundle.BundleId
			doc.brand_id=bundle.BrandId
			doc.network=bundle.Network
			doc.description=bundle.Description
			doc.insert()

			amount = int(bundle.Amount) / 100

			new_name = f'{bundle.Name}-({bundle.ValidityPeriod} days) (ZWL ${amount})'

			if convert:
				new_amount = round(rate * amount, 2)
				new_name = f'{bundle.Name}-({bundle.ValidityPeriod} days) (ZWL ${amount}) - ({curr} ${new_amount})'

			frappe.rename_doc('EconetBundle', doc.name, new_name)

		except Exception as err:
			continue

@frappe.whitelist()
def delete_all_data():
	'''
		delete all previously added bundles data
	'''
	bundles = frappe.get_list('EconetBundle', limit_page_length=100)

	for bndl in bundles:
		try:
			b = frappe.get_doc('EconetBundle', bndl.name)
			b.delete()
			
		except:
			continue

@frappe.whitelist()
def get_all_data():
	'''
		get all previously added bundles data
	'''
	bundles = frappe.get_list('EconetBundle', limit_page_length=100)

	filtered = []

	for bundle in bundles:
		b = frappe.get_doc('EconetBundle', bundle.name)
		if b.network == 'Econet WhatsApp':
			filtered.append(b)

	return filtered

@frappe.whitelist()
def get_all_data_filtered(filter_by=None):
	'''
		get all previously added bundles data
	'''
	bundles = frappe.get_list('EconetBundle', limit_page_length=100)

	filtered = []

	if filter_by is None:
		filter_by = 'Econet Data'

	for bundle in bundles:
		b = frappe.get_doc('EconetBundle', bundle.name)
		if b.network == filter_by:
			filtered.append(bundle.name)

	return filtered