
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
class Vehiculo(models.Model):
    _name = 'taller.vehiculo'
    _description = 'Vehículo'

    matricula = fields.Char(string="Matrícula", required=True)
    numero_chasis = fields.Char(string="Número de chasis", required=True, index=True)
    marca = fields.Char()
    modelo = fields.Char()
    fecha_matriculacion = fields.Date(string="Fecha de matriculación")
    cliente_id = fields.Many2one('res.partner',string="Propietario",required=True)
    
    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.matricula or ''} - {rec.marca or ''} {rec.modelo or ''}"
            result.append((rec.id, name))
        return result



    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('matricula', operator, name), ('numero_chasis', operator, name)]
        return self.search(domain + args, limit=limit).name_get()

    @api.constrains('matricula', 'fecha_matriculacion')
    def _check_matricula(self):
    # SOLO VALIDAR, NO MODIFICAR campos
        for record in self:
            if not record.matricula:
                raise ValidationError("La matrícula no puede estar vacía.")
            if not record.fecha_matriculacion:
                raise ValidationError("La fecha de matriculación es obligatoria para validar la matrícula.")

            matricula = record.matricula.upper()
            year = record.fecha_matriculacion.year

            # Validar según año...
            # sin modificar record.matricula aquí

    @api.constrains('numero_chasis')
    def _check_numero_chasis(self):
        pattern = r'^[A-HJ-NPR-Z0-9]{17}$'  # Excluye I, O, Q
        for record in self:
            if not record.numero_chasis:
                raise ValidationError("El número de chasis no puede estar vacío.")
            if not re.match(pattern, record.numero_chasis.upper()):
                raise ValidationError("El número de chasis debe tener exactamente 17 caracteres alfanuméricos sin I, O ni Q.")

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

    @api.constrains('cliente_id')
    def _check_cliente_id(self):
        for record in self:
            if not record.cliente_id.email:
                raise ValidationError(f"El propietario {record.cliente_id.name} debe tener un correo electrónico válido.")

    def _to_upper(self, vals, campos):
        for campo in campos:
            if campo in vals and isinstance(vals[campo], str):
                vals[campo] = vals[campo].upper()
        return vals

    @api.model
    def create(self, vals):
        vals = self._to_upper(vals, ['matricula', 'numero_chasis', 'marca', 'modelo'])
        return super().create(vals)

    def write(self, vals):
        vals = self._to_upper(vals, ['matricula', 'numero_chasis', 'marca', 'modelo'])
        return super().write(vals)

