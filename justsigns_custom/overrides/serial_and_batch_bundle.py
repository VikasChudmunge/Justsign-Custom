# Copyright (c) 2025, MithTech and contributors
# For license information, please see license.txt

import frappe
from frappe import bold
from frappe.utils import flt

from erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle import (
	SerialandBatchBundle as ERPSerialandBatchBundle,
)


class SerialandBatchBundle(ERPSerialandBatchBundle):
	def validate_quantity(self, row, qty_field=None):
		qty_field = self.get_qty_field(row, qty_field=qty_field)
		qty = row.get(qty_field)

		if qty_field == "qty" and row.get("stock_qty"):
			qty = row.get("stock_qty")
		elif qty_field == "rejected_qty":
			qty = self.get_rejected_stock_qty(row, qty)

		precision = row.precision
		if abs(abs(flt(self.total_qty, precision)) - abs(flt(qty, precision))) > 0.01:
			total_qty = frappe.format_value(abs(flt(self.total_qty)), "Float", row)
			set_qty = frappe.format_value(abs(flt(row.get(qty_field))), "Float", row)
			self.throw_error_message(
				f"Total quantity {total_qty} in the Serial and Batch Bundle {bold(self.name)} "
				f"does not match with the quantity {set_qty} for the Item {bold(self.item_code)} "
				f"in the {self.voucher_type} # {self.voucher_no}"
			)

	def get_rejected_stock_qty(self, row, qty):
		conversion_factor = row.get("conversion_factor")
		if conversion_factor:
			return flt(qty) * flt(conversion_factor)

		return qty
