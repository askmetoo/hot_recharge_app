// Copyright (c) 2021, DonnC Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recharge Zesa', {
	// refresh: function(frm) {

	// }
	check_customer: function (frm) {
		var m = frm.doc.meter_number

		if (m) {
			if (m === "") {
				frappe.throw(__('meter number is required!'));
			}

			else {
				frm.call({
					method: "hot_recharge_app.hot_recharge_app.doctype.zesacustomer.zesacustomer.fetch_zesa_customer",
					args: {
						"meter_number": frm.doc.meter_number
					},
					callback: function (r) {
						var result = r.message;

						if (result) {
							frappe.confirm('Confirm that meter: ' + result['meter_number'] + ' is for ' + result['name1'] + '?',
								() => {
									// action to perform if Yes is selected
									frm.set_value({
										'customer': result['name1'],
										'address': result['address'],
										'meter_number': result['meter_number']
									});
								},
								() => {
									// action to perform if No is selected
									frm.set_value({
										'customer': null,
										'address': null
									});
									frappe.msgprint(__('Double check customer meter number and check again!'));
								}
							);
						}
					}
				});
			}
		}
	},
});