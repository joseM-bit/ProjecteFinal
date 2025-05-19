from odoo import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'
    
    
    vehiculo_ids = fields.One2many('taller.vehiculo','cliente_id',string="Vehículos del cliente",readonly=True)

    

