from odoo import models, fields, api

class Empleado(models.Model):
    _inherit = 'hr.employee'

    puesto_taller = fields.Selection(
        [('mecanico', 'Mecánico'), ('jefe_taller', 'Jefe de Taller'), ('recepcionista', 'Recepcionista')],
        string="Puesto en el Taller",
        required=True
    )
