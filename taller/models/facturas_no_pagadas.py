from odoo import models, fields, api

class FacturasNoPagadasWizard(models.TransientModel):
    _name = 'facturas.nopagadas.wizard'
    _description = 'Wizard para mostrar facturas no pagadas'

    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True)
    factura_ids = fields.Many2many('account.move', string='Facturas no pagadas')
    move_id = fields.Many2one('account.move',string='Factura',default=lambda self: self.env.context.get('active_id'))
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        factura = self.env['account.move'].browse(active_id)

        if factura.move_type == 'out_invoice' and factura.partner_id:
            facturas_no_pagadas = self.env['account.move'].search([
                ('partner_id', '=', factura.partner_id.id),
                ('move_type', '=', 'out_invoice'),
                ('payment_state', '!=', 'paid'),
                ('state', '=', 'posted'),
            ])
            res.update({
                'partner_id': factura.partner_id.id,
                'factura_ids': [(6, 0, facturas_no_pagadas.ids)],
            })
        return res

    def action_mostrar_facturas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facturas No Pagadas',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [
                ('partner_id', '=', self.move_id.partner_id.id),
                ('payment_state', '!=', 'paid'),
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted') 
            ],
            'context': {'search_default_unpaid': 1}
        }
    

