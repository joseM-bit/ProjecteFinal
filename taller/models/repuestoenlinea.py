from odoo import models, fields, api
from odoo.exceptions import ValidationError

class OrdenRepuestoLine(models.Model):
    _name = 'taller.orden.repuesto.line'
    _description = 'Línea de Repuesto en Orden'

    orden_id = fields.Many2one('taller.orden', string='Orden', ondelete='cascade', required=True)
    producto_id = fields.Many2one('product.product', string='Producto', required=True)
    cantidad = fields.Float(string='Cantidad', default=1.0)

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        # Ejemplo simple: si quieres llenar automáticamente algo al elegir producto
        if self.producto_id:
            # Por ejemplo, podrías poner un valor por defecto en cantidad
            self.cantidad = 1.0
        else:
            self.cantidad = 0
    @api.constrains('producto_id', 'cantidad')
    def _check_stock_taller(self):
        for line in self:
            # Usar stock físico real (qty_available) en lugar de stock_taller
            stock_disponible = line.producto_id.qty_available
            if stock_disponible < line.cantidad:
                raise ValidationError(
                    f"No hay suficiente stock para {line.producto_id.display_name}. Stock disponible: {stock_disponible}"
                )
