// Copyright (c) 2021, DonnC Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rechange Bundle', {
	// refresh: function(frm) {

	// }
	onload: function(frm, cdt, cdn) {
		frm.call({
			method: "hot_recharge_app.hot_recharge_app.doctype.recharge_econet_bundle.recharge_econet_bundle.get_econet_bundles",
			callback: function (r) {
				console.log(r.message);
				var result_array = r.message;

				//frappe.model.set_value(cdt, cdn, 'bundle', result_array);
				//frm.set_value({'bundle': result_array});
				//frappe.meta.get_docfield(cdt, 'bundle').options = result_array;
				//frm.set_df_property('expense_account', 'options', ['option a', 'option b']);
				frm.set_df_property('bundle', 'options', result_array);
			}
		});
	},
});
