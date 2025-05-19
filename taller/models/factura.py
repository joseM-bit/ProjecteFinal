from odoo import models, fields, api

class Factura(models.Model):
    _inherit = 'account.move'

    kilometros = fields.Integer(string="Kilómetros vehículo")
    vehiculo_ids = fields.Many2many(
        'taller.vehiculo',
        string="Vehículos relacionados",
        relation='factura_vehiculo_rel',  # 🔄 Añade una tabla de relación explícita
        column1='factura_id',
        column2='vehiculo_id'
    )

    @api.depends('partner_id')
    def _compute_vehiculo_ids(self):
        for move in self:
            if move.partner_id:
                # Buscar vehículos asociados al cliente
                move.vehiculo_ids = self.env['taller.vehiculo'].search([
                    ('cliente_ids', 'in', move.partner_id.ids)
                ])
            else:
                move.vehiculo_ids = False  # Limpiar si no hay cliente

