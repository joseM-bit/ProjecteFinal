from odoo import models, fields, api

class Factura(models.Model):
    _name ='account.move'
    _inherit = 'account.move'

    vehiculo_ids = fields.Many2many(
        'taller.vehiculo',
        string="Vehículos relacionados",
        compute='_compute_vehiculo_ids',
        store=False
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

