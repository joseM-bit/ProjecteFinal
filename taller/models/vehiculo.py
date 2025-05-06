from odoo import models, fields, api
from odoo.exceptions import ValidationError  # Asegúrate de importar esto

class Vehiculo(models.Model):
    _name = 'taller.vehiculo'
    _description = 'Vehículo'

    matricula = fields.Char(string="Matrícula", required=True)
    numero_chasis = fields.Char(string="Número de chasis", required=True, index=True)
    marca = fields.Char()
    modelo = fields.Char()
    ano = fields.Integer(string="Año")
    cliente_ids = fields.Many2many('res.partner', string="Propietarios")

    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.matricula or ''} - {rec.marca or ''} {rec.modelo or ''} ({rec.ano or ''})"
            result.append((rec.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('matricula', operator, name), ('numero_chasis', operator, name)]
        return self.search(domain + args, limit=limit).name_get()

    @api.constrains('matricula')
    def _check_matricula(self):
        for record in self:
            if not record.matricula:
                raise ValidationError("La matrícula no puede estar vacía.")
            if len(record.matricula) < 5:
                raise ValidationError("La matrícula debe tener al menos 5 caracteres.")
            if not record.matricula.isalnum():
                raise ValidationError("La matrícula solo puede contener caracteres alfanuméricos.")

    @api.constrains('numero_chasis')
    def _check_numero_chasis(self):
        for record in self:
            if not record.numero_chasis:
                raise ValidationError("El número de chasis no puede estar vacío.")
            if len(record.numero_chasis) < 5:
                raise ValidationError("El número de chasis debe tener al menos 5 caracteres.")
            if not record.numero_chasis.isalnum():
                raise ValidationError("El número de chasis solo puede contener caracteres alfanuméricos.")

    @api.constrains('ano')
    def _check_ano(self):
        for record in self:
            if record.ano and (record.ano < 1886 or record.ano > fields.Date.today().year):
                raise ValidationError("El año debe estar entre 1886 y el año actual.")

    @api.constrains('marca')
    def _check_marca(self):
        for record in self:
            if not record.marca:
                raise ValidationError("La marca no puede estar vacía.")
            if len(record.marca) < 2:
                raise ValidationError("La marca debe tener al menos 2 caracteres.")
            if not record.marca.isalpha():
                raise ValidationError("La marca solo puede contener letras.")

    @api.constrains('modelo')
    def _check_modelo(self):
        for record in self:
            if not record.modelo:
                raise ValidationError("El modelo no puede estar vacío.")
            if len(record.modelo) < 2:
                raise ValidationError("El modelo debe tener al menos 2 caracteres.")
            if not record.modelo.isalnum():
                raise ValidationError("El modelo solo puede contener caracteres alfanuméricos.")

    @api.constrains('cliente_ids')
    def _check_cliente_ids(self):
        for record in self:
            if not record.cliente_ids:
                raise ValidationError("El vehículo debe tener al menos un propietario.")
            if len(record.cliente_ids) > 5:
                raise ValidationError("El vehículo no puede tener más de 5 propietarios.")
            for cliente in record.cliente_ids:
                if not cliente.email:
                    raise ValidationError(f"El propietario {cliente.name} debe tener un correo electrónico válido.")
