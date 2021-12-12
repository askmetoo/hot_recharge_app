// Copyright (c) 2021, DonnC Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Zesa Balance', {
	refresh_btn: function(frm, cdt, cdn) {
		frappe.show_alert('fetching current balance..', 3);
		
		frm.call({
			method: "hot_recharge_app.hot_recharge_app.doctype.zesa_balance.zesa_balance.get_zesa_balance",
			callback: function (r) {
				var res = r.message;

				if(res) {
					frappe.model.set_value(cdt, cdn, 'wallet_balance', res);
					frappe.model.set_value(cdt, cdn, 'last_refreshed', frappe.datetime.now_datetime());
				}
			}
		});
	},
});
