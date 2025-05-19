from odoo import models, fields, api

class Stock(models.Model):
    
    _inherit = "stock.picking"  # Hereda de stock.picking (ajusta según tu necesidad)
    _description = "Modelo Personalizado de Stock"
    
    x_custom_priority = fields.Selection(
        [('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta')],
        string="Prioridad Personalizada",
        default='medium'
    )
    x_notes = fields.Text(string="Notas Adicionales")
