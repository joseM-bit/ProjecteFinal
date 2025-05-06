from odoo import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    vehiculo_ids = fields.Many2many(
    'taller.vehiculo', 
    compute='_compute_vehiculos',
    string="Vehículos",
    store=False
    )

    def _compute_vehiculos(self):
        for partner in self:
            partner.vehiculo_ids = self.env['taller.vehiculo'].search([('cliente_ids', 'in', partner.id)])

