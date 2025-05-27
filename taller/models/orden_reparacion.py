from odoo import models, fields
from odoo.exceptions import ValidationError


class OrdenReparacion(models.Model):
    _name = 'taller.orden'
    _description = 'Orden de Reparación'

    vehiculo_id = fields.Many2one('taller.vehiculo', string="Vehículo", required=True)
    tecnico_id = fields.Many2one('hr.employee', string="Técnico",required=True,ondelete='restrict')
    descripcion = fields.Text()
    fecha_inicio = fields.Date()
    fecha_fin = fields.Date()
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado')
    ], default='pendiente')
    factura_id = fields.Many2one('account.move', string="Factura")
    factura_numero = fields.Char(string="Número de factura", related='factura_id.name', readonly=True)
    
    kilometros = fields.Integer(string="Kilómetros")
    repuesto_ids = fields.One2many('taller.orden.repuesto.line', 'orden_id', string="Repuestos usados")

    def action_open_factura(self):
        self.ensure_one()
        if not self.factura_id:
            return {'type': 'ir.actions.act_window_close'}
        return {
            'type': 'ir.actions.act_window',
            'name': 'Factura',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.factura_id.id,
            'target': 'current',
        }
    def crear_factura(self):
        self.ensure_one()
        if self.factura_id:
            raise ValidationError("Ya hay una factura asociada a esta orden.")

        if not self.vehiculo_id.cliente_id:
            raise ValidationError("El vehículo no tiene un propietario asignado.")

        # Crear factura base
        factura = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.vehiculo_id.cliente_id.id,
            'invoice_origin': f"Orden de Reparación #{self.id}",
            'invoice_date': fields.Date.today(),
            'vehiculo_ids': [(6, 0, [self.vehiculo_id.id])],
            'kilometros': self.kilometros,
        })

        # Añadir líneas por repuestos usados
        for linea in self.repuesto_ids:
            factura.invoice_line_ids.create({
                'move_id': factura.id,
                'product_id': linea.producto_id.id,
                'name': linea.producto_id.display_name,
                'quantity': linea.cantidad,
                'price_unit': linea.producto_id.lst_price,
                'tax_ids': [(6, 0, linea.producto_id.taxes_id.ids)],
            })

        self.factura_id = factura.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': factura.id,
            'target': 'current',
        }