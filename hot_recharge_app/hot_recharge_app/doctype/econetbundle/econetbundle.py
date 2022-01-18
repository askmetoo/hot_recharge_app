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
	data_rate = settings.get('data_rate', 1)
	
	for bundle in bundles:
		# exclude all daily bundles 
		if int(bundle.ValidityPeriod) < 3:
			continue

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

			new_name = f'{bundle.Name}-({bundle.ValidityPeriod} days) (${amount})'

			if convert:
				# check if its private wifi bundle PWBxx
				# if so, apply data_rate
				if str(bundle.ProductCode).startswith('PWB'):
					new_amount = round(amount / data_rate, 0)
					new_name = f'{bundle.Name}-({bundle.ValidityPeriod} days) (${amount})-(R{new_amount})'

				else:
					new_amount = round(amount / rate, 0)
					new_name = f'{bundle.Name}-({bundle.ValidityPeriod} days) (${amount})-(R{new_amount})'

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
def get_all_data_filtered(filter_by=None, external_api=False):
	'''
		get all previously added bundles data by filter passed
		external_api: True > a list of dict
					  False > a list of names
	'''
	bundles = frappe.get_list('EconetBundle', limit_page_length=100)

	filtered = []
	for_external = []

	if filter_by is None:
		filter_by = 'Econet Data'

	if len(bundles) == 0:
		return None

	for bundle in bundles:
		b = frappe.get_doc('EconetBundle', bundle.name)
		if b.network == filter_by:
			filtered.append(bundle.name)
			for_external.append(b.as_dict())

	if external_api:
		return for_external

	return filtered