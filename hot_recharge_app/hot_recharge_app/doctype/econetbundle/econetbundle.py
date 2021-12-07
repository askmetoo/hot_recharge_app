# Copyright (c) 2021, DonnC Lab and contributors
# For license information, please see license.txt

import frappe
from munch import Munch
from frappe.model.document import Document

class EconetBundle(Document):
	pass


# TODO can put conversion rates here for balance 
# or another currency
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

			frappe.rename_doc('EconetBundle', doc.name, f'{bundle.Name}-{bundle.ValidityPeriod} ({bundle.Amount})')
			doc.reload()

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
def get_all_data_filtered():
	'''
		get all previously added bundles data
	'''
	bundles = frappe.get_list('EconetBundle', limit_page_length=100)

	filtered = []

	for bundle in bundles:
		# b = frappe.get_doc('EconetBundle', bundle.name)
		# if b.network == 'Econet WhatsApp':
		# 	filtered.append(bundle.name)
		filtered.append(bundle.name)

	return filtered