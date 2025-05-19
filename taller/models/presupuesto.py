from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Presupuesto(models.Model):
    _inherit = 'sale.order'

    vehiculo_ids = fields.Many2many(
        'taller.vehiculo',
        relation='sale_order_vehiculo_rel',  # 🔄 Tabla de relación única
        column1='sale_order_id',
        column2='vehiculo_id',
        string='Vehículos relacionados'
    )
    kilometros = fields.Integer(string='Kilómetros del Vehículo')
    
    def crear_factura(self):
        action = self._create_invoices()
        return action

    def _create_invoices(self, grouped=False, final=False):
        return super()._create_invoices(grouped=grouped, final=final)
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'vehiculo_ids': [(6, 0, self.vehiculo_ids.ids)],
            'kilometros': self.kilometros,
        })
        return invoice_vals