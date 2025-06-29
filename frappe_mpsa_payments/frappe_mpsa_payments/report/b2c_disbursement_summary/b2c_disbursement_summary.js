// Copyright (c) 2025, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["B2C Disbursement Summary"] = {
	"filters": [
		{
			"fieldname": "party",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"options": "party_type"
		},
		{
			"fieldname": "party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "Doctype"
		},
		{
			"fieldname": "posting_date",
			"label": __("Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "transaction_to_pay_against",
			"label": __("Transaction"),
			"fieldtype": "Link",
			"options": "Doctype"
		},

	]
};
