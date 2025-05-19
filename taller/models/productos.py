from odoo import models, fields, api

class Productos(models.Model):
    _inherit = 'product.product'
    _description = 'Productos para Taller'

    
    tipo_repuesto = fields.Selection([
        ('original', 'Original'),
        ('generico', 'Genérico'),
    ], string="Tipo de Repuesto")
    stock_taller = fields.Float(
        string="Stock reservado para taller",
        compute='_compute_stock_taller',
        store=True
    )
    
    @api.depends('qty_available')
    def _compute_stock_taller(self):
        for product in self:
            product.stock_taller = product.qty_available  # Vincula al stock físico
