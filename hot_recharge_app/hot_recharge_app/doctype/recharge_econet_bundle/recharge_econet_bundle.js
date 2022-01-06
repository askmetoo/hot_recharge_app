// Copyright (c) 2021, DonnC Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recharge Econet Bundle', {
	refresh: function (frm) {
		frm.add_custom_button(__("Refresh Bundle List"), function () {
			frm.disable_save();

			frappe.show_alert('getting available data bundles list..', 5);
			
			frm.call({
				method: "hot_recharge_app.hot_recharge_app.doctype.recharge_econet_bundle.recharge_econet_bundle.get_econet_bundles",
				callback: function (r) {
					var res = r.message;

					if (res) {
						frappe.msgprint({
							title: __('Bundles'),
							indicator: 'green',
							message: __("data bundles list refreshed!")
						});
						frm.refresh_field('bundle');
						frm.enable_save();
					}
				}
			});
		});
	},
	onload: function(frm, cdt, cdn) {
		frm.call({
			method: "hot_recharge_app.hot_recharge_app.doctype.econetbundle.econetbundle.get_all_data_filtered",
			args: {
				"filter_by": frm.doc.package
			},
			callback: function (r) {
				console.log(r.message);
				var result_array = r.message;

				if(result_array != null) {
					frm.set_df_property('bundle', 'options', result_array);
				}

				else {
					frappe.msgprint({
						title: __('Bundles'),
						indicator: 'red',
						message: __("no bundles found. Use the bundle refresh button to load list")
					});
				}
			}
		});
	},
	package: function(frm, cdt, cdn) {
		frm.call({
			method: "hot_recharge_app.hot_recharge_app.doctype.econetbundle.econetbundle.get_all_data_filtered",
			args: {
				"filter_by": frm.doc.package
			},
			callback: function (r) {
				console.log(r.message);
				var result_array = r.message;

				if(result_array != null) {
					frm.set_df_property('bundle', 'options', result_array);
				}

				else {
					frappe.msgprint({
						title: __('Bundles'),
						indicator: 'red',
						message: __("no bundles found. Use the bundle refresh button to load list")
					});
				}
			}
		});
	},
});
