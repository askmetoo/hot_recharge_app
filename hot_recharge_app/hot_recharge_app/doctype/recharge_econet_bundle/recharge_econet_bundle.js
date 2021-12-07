// Copyright (c) 2021, DonnC Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recharge Econet Bundle', {
	// refresh: function(frm) {

	// }
	onload: function(frm, cdt, cdn) {
		frm.call({
			method: "hot_recharge_app.hot_recharge_app.doctype.recharge_econet_bundle.recharge_econet_bundle.get_econet_bundles",
			callback: function (r) {
				console.log(r.message);
				var result_array = r.message;

				frappe.model.set_value(cdt, cdn, 'bundle', result_array);
			}
		});
	},
});
