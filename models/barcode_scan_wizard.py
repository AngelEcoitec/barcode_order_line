# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class BarcodeScanWizard(models.TransientModel):
    _name = "barcode.scan.wizard"
    _description = "Wizard para escanear código de barras y agregar productos al pedido"

    barcode = fields.Char(string="Código de Barras", required=True)

    def action_process_barcode(self):
        self.ensure_one()
        product = self.env["product.product"].search([("barcode", "=", self.barcode)], limit=1)
        if not product:
            raise UserError(_("No se encontró ningún producto con el código %s.") % self.barcode)
    
        # Detecta el modelo activo desde el contexto
        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        if not active_model or not active_id:
            raise UserError(_("No se pudo determinar el documento activo."))
    
        record = self.env[active_model].browse(active_id)
    
        if active_model == "sale.order":
            # Lógica para pedido de venta:
            order_line = record.order_line.filtered(lambda l: l.product_id == product)
            if order_line:
                order_line.product_uom_qty += 1
            else:
                order_line_vals = {
                    "order_id": record.id,
                    "product_id": product.id,
                    "product_uom_qty": 1,
                    "price_unit": product.lst_price,
                }
                record.order_line = [(0, 0, order_line_vals)]
        elif active_model == "stock.picking":
            # Lógica para traspaso interno:  
            # Por ejemplo, buscar o crear una línea de movimiento para ese producto
            move_line = record.move_line_ids.filtered(lambda l: l.product_id == product)
            if move_line:
                move_line.quantity += 1
            else:
                move_line_vals = {
                    "picking_id": record.id,
                    "product_id": product.id,
                    "quantity": 1,
                    # Agrega otros valores necesarios, como ubicaciones
                }
                record.move_line_ids = [(0, 0, move_line_vals)]
        else:
            raise UserError(_("El modelo activo %s no está soportado para el escaneo de códigos.") % active_model)
    
        return {"type": "ir.actions.act_window_close"}

