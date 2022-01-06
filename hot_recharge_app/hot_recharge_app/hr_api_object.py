import hotrecharge
import uuid

import frappe

import phonenumbers as pn

@frappe.whitelist()
def number_parser(number):
	try:
		num = pn.parse(number, 'ZW')

		nf = num.national_number

        # add leading zero for zim numbers
		return f'0{nf}'

	except Exception as err:
		print(err)
		return None

@frappe.whitelist()
def get_hr_api_object() -> hotrecharge.HotRecharge:
    settings = get_hr_settings()

    if type(settings) is int:
        return settings

    config = hotrecharge.HRAuthConfig(
        access_code= settings.get('access_code'), 
        access_password=settings.get('access_password'),
        reference= settings.get('reference_prefix') + str(uuid.uuid4())
    )

    api = hotrecharge.HotRecharge(config, return_model=True)

    return api

@frappe.whitelist()
def get_hr_settings() -> dict:
    '''
     take hot recharge set settings from desk
    '''
    doc = frappe.get_single('Hot Recharge Settings')

    pwd = doc.get_password('access_password')

    _copy = doc.as_dict()

    _copy['access_password'] = pwd

    return _copy