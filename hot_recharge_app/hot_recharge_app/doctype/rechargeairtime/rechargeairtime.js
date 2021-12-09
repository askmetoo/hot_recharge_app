// Copyright (c) 2021, DonnC Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on('RechargeAirtime', {
	refresh: function (frm) {
		
		frm.add_custom_button(__("Query Transaction"), function () {
			frappe.show_alert('making transaction query request..', 5);

			frm.call({
				method: "hot_recharge_app.hot_recharge_app.doctype.rechargeairtime.rechargeairtime.query",
				args: {
					"reference": frm.doc.reference
				},
				callback: function (r) {
					var result = r.message;
					console.log(result);

					if (result) {
						frappe.msgprint({
							title: __('Query'),
							indicator: 'green',
							message: __(result)
						});
					}
				}
			});
		});
	}
});