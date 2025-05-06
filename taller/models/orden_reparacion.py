from odoo import models, fields

class OrdenReparacion(models.Model):
    _name = 'taller.orden'
    _description = 'Orden de Reparación'

    vehiculo_id = fields.Many2one('taller.vehiculo', string="Vehículo", required=True)
    tecnico_id = fields.Many2one('res.users', string="Técnico")
    descripcion = fields.Text()
    fecha_inicio = fields.Date()
    fecha_fin = fields.Date()
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado')
    ], default='pendiente')
    factura_id = fields.Many2one('account.move', string="Factura")
    repuesto_ids = fields.Many2many('product.product', string="Repuestos usados")