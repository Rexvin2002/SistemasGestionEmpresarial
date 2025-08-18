# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re

class Psicologo(models.Model):
    _name = 'psicologia.psicologo'
    _description = 'Psicologos'

    # HEADER
    imagen = fields.Binary(string='Imagen del/la Psicologo/a')
    name = fields.Char(string="Nombre y Apellidos", required=True)
    numero_colegiado = fields.Char(string="Número de Colegiado", required=True)

    # DATOS PERSONALES
    dni = fields.Char(string="DNI", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    edad = fields.Integer(string="Edad", compute="_compute_edad", store=True, readonly=True)
    telefono = fields.Char(string="Teléfono")
    correo = fields.Char(string="Correo Electrónico")
    direccion = fields.Char(string="Dirección")

    # NOTEBOOK
    pacientes_ids = fields.Many2many('psicologia.paciente', 'psicologo_id', string="Pacientes")
    terapias_ids = fields.Many2many('psicologia.terapia', 'id_terapia', string="Terapias")

    total_pacientes = fields.Integer(string="Total de Pacientes", compute="_compute_total_pacientes", store=True)
    total_terapias = fields.Integer(string="Total de Terapias", compute="_compute_total_terapias", store=True)

    # MÉTODOS
    @api.constrains('dni')
    def _check_dni(self):
        """ Valida que el DNI sea correcto según el formato español """
        dni_regex = r'^\d{8}[A-Z]$'
        valid_letters = "TRWAGMYFPDXBNJZSQVHLCKE"

        for record in self:
            dni = record.dni.upper().strip()  # Normalizamos el DNI
            if not re.match(dni_regex, dni):
                raise ValidationError("El DNI debe tener 8 números seguidos de una letra mayúscula (Ej: 12345678Z).")

            num = int(dni[:-1])  # Tomamos los 8 números
            letter = dni[-1]  # Tomamos la letra final
            if valid_letters[num % 23] != letter:
                raise ValidationError("La letra del DNI no es correcta.")

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        today = date.today()
        for record in self:
            if record.fecha_nacimiento:
                record.edad = today.year - record.fecha_nacimiento.year - \
                              ((today.month, today.day) < (record.fecha_nacimiento.month, record.fecha_nacimiento.day))
            else:
                record.edad = 0

    @api.constrains('telefono')
    def _check_telefono(self):
        pattern = re.compile(r'^[6789]\d{8}$')
        for record in self:
            if record.telefono and not pattern.match(record.telefono):
                raise ValidationError("El teléfono debe tener 9 dígitos y comenzar con 6, 7, 8 o 9.")  

    @api.depends('pacientes_ids')
    def _compute_total_pacientes(self):
        for record in self:
            record.total_pacientes = len(record.pacientes_ids)

    @api.depends('terapias_ids')
    def _compute_total_terapias(self):
        for record in self:
            record.total_terapias = len(record.terapias_ids)

class Paciente(models.Model):
    _name = 'psicologia.paciente'
    _description = 'Paciente'

    # HEADER
    imagen = fields.Binary(string='Imagen del/la Paciente')
    name = fields.Char(string="Nombre y Apellidos", required=True)
    
    # DATOS PERSONALES
    dni = fields.Char(string="DNI", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")  
    edad = fields.Integer(string="Edad", compute="_compute_edad", store=True, readonly=True)
    telefono = fields.Char(string="Teléfono")
    correo = fields.Char(string="Correo Electrónico")
    direccion = fields.Char(string="Dirección")
    historial_medico = fields.Text(string="Historial Médico")

    # CORRESPONDENCIAS
    psicologo_ids = fields.Many2many('psicologia.psicologo', string="Psicólogos Asignados")
    
    # NOTEBOOK
    terapias_ids = fields.Many2many('psicologia.terapia', string="Terapia")
    total_terapias = fields.Integer(string="Total de Terapias", compute="_compute_total_terapias", store=True)
    
    # MÉTODOS
    @api.constrains('dni')
    def _check_dni(self):
        """ Valida que el DNI sea correcto según el formato español """
        dni_regex = r'^\d{8}[A-Z]$'
        valid_letters = "TRWAGMYFPDXBNJZSQVHLCKE"

        for record in self:
            dni = record.dni.upper().strip()  # Normalizamos el DNI
            if not re.match(dni_regex, dni):
                raise ValidationError("El DNI debe tener 8 números seguidos de una letra mayúscula (Ej: 12345678Z).")

            num = int(dni[:-1])  # Tomamos los 8 números
            letter = dni[-1]  # Tomamos la letra final
            if valid_letters[num % 23] != letter:
                raise ValidationError("La letra del DNI no es correcta.")

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        today = date.today()
        for record in self:
            if record.fecha_nacimiento:
                record.edad = today.year - record.fecha_nacimiento.year - \
                              ((today.month, today.day) < (record.fecha_nacimiento.month, record.fecha_nacimiento.day))
            else:
                record.edad = 0

    @api.constrains('telefono')
    def _check_telefono(self):
        pattern = re.compile(r'^[6789]\d{8}$')
        for record in self:
            if record.telefono and not pattern.match(record.telefono):
                raise ValidationError("El teléfono debe tener 9 dígitos y comenzar con 6, 7, 8 o 9.")

    @api.depends('terapias_ids')
    def _compute_total_terapias(self):
        """ Calcula el total de terapias asociadas al paciente """
        for record in self:
            record.total_terapias = len(record.terapias_ids)

class Sesion(models.Model):
    _name = 'psicologia.sesion'
    _description = 'Sesión'

    name = fields.Char(string="ID", required=True, default='Nuevo', readonly=True)

    # CORRESPONDENCIAS
    terapia_id = fields.Many2one('psicologia.terapia', string="Terapia")
    factura_id = fields.Many2one('psicologia.factura', string="Factura", required=True, ondelete='restrict', domain="[('id', '!=', False)]")

    # FECHA Y DURACIÓN
    fecha_hora = fields.Datetime(string="Fecha y hora", required=True, default=fields.Datetime.now)
    duracion = fields.Float(string="Duración (horas)")

    # INFORMACIÓN ADICIONAL
    diagnostico = fields.Text(string="Diagnóstico")
    notas = fields.Text(string="Notas de la Sesión")
    
    # NOTEBOOK
    tratamiento_ids = fields.Many2many('psicologia.tratamiento', string="Tratamientos Aplicados")
    total_tratamientos = fields.Integer(string="Total de Tratamientos", compute="_compute_totales", store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('psicologia.sesion') or 'Nuevo'
        return super(Sesion, self).create(vals)

    @api.depends('tratamiento_ids')  # Aquí debe depender de tratamiento_ids
    def _compute_totales(self):
        for record in self:
            record.total_tratamientos = len(record.tratamiento_ids)

class Tratamiento(models.Model):
    _name = 'psicologia.tratamiento'
    _description = 'Tratamiento'

    id_tratamiento = fields.Char(string="ID", required=True, default='Nuevo')
    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")

    # MÉTODOS
    @api.model
    def create(self, vals):
        if vals.get('id_tratamiento', 'Nuevo') == 'Nuevo':
            vals['id_tratamiento'] = self.env['ir.sequence'].next_by_code('psicologia.tratamiento') or 'Nuevo'
        return super(Tratamiento, self).create(vals)

class Factura(models.Model):
    _name = 'psicologia.factura'
    _description = 'Factura'

    # HEADER
    estado = fields.Selection([
        ('pendiente', 'Pendiente de pago'),
        ('cancelada', 'Cancelada'),
        ('pagado', 'Pagado')
    ], string="Estado", default='pendiente')

    name = fields.Char(string="ID", required=True, default='Nuevo', readonly=True)

    # CORRESPONDENCIAS
    paciente_id = fields.Many2one('psicologia.paciente', string="Paciente", required=True)
    sesion_ids = fields.One2many('psicologia.sesion', 'factura_id', string="Sesiones")
    
    # FECHA Y DURACIÓN
    fecha_emision = fields.Date(string="Fecha de Emisión", required=True, default=lambda self: date.today())
    
    # INFORMACIÓN ADICIONAL
    currency_id = fields.Many2one('res.currency', string="Moneda", default=lambda self: self.env.company.currency_id)
    total = fields.Monetary(string="Total", required=True, currency_field='currency_id')
    
    # MÉTODOS
    def action_pendiente(self):
        self.write({'estado': 'pendiente'})
    
    def action_pagado(self):
        self.write({'estado': 'pagado'})
    
    def action_cancelada(self):
        self.write({'estado': 'cancelada'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('psicologia.factura') or 'Nuevo'
        return super(Factura, self).create(vals)

class Terapia(models.Model):
    _name = 'psicologia.terapia'
    _description = 'Terapias'

    # HEADER
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada')
    ], string="Estado", default='pendiente')

    name = fields.Char(string="ID de Terapia", required=True, default='Nuevo', readonly=True)

    # CORRESPONDENCIAS
    paciente_id = fields.Many2one('psicologia.paciente', string="Paciente", required=True)
    psicologo_ids = fields.Many2many('psicologia.psicologo', string="Psicólogos")
    
    # FECHA Y DURACIÓN
    fecha = fields.Date(string="Fecha", required=True)
    duracion = fields.Float(string="Duración Total (horas)", compute="_compute_duracion", store=True, readonly=True)
    
    # NOTEBOOK
    total_sesiones = fields.Integer(string="Total de Sesiones", compute='_compute_total_sesiones', store=True)
    sesion_ids = fields.One2many('psicologia.sesion', 'terapia_id', string="Sesiones")

    # MÉTODOS
    def action_pendiente(self):
        self.write({'estado': 'pendiente'})

    def action_confirmada(self):
        self.write({'estado': 'confirmada'})

    def action_cancelada(self):
        self.write({'estado': 'cancelada'})

    def action_completada(self):
        self.write({'estado': 'completada'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('psicologia.terapia') or 'Nuevo'
        return super(Terapia, self).create(vals)

    @api.depends('sesion_ids.duracion')
    def _compute_duracion(self):
        for record in self:
            record.duracion = sum(record.sesion_ids.mapped('duracion'))

    @api.depends('sesion_ids')
    def _compute_total_sesiones(self):
        for record in self:
            record.total_sesiones = len(record.sesion_ids)

class WizardAsignarPacientes(models.TransientModel):
    _name = 'psicologia.asignar.pacientes.wizard'
    _description = 'Asignar Pacientes a Psicólogo'

    psicologo_id = fields.Many2one('psicologia.psicologo', string="Psicólogo", required=True)
    paciente_ids = fields.Many2many('psicologia.paciente', string="Pacientes a Asignar")

    def action_asignar_pacientes(self):
        if not self.paciente_ids:
            raise ValidationError("Debes seleccionar al menos un paciente.")
        self.psicologo_id.pacientes_ids = [(4, paciente.id) for paciente in self.paciente_ids]
        for paciente in self.paciente_ids:
            paciente.psicologo_ids = [(4, self.psicologo_id.id)]

class WizardCrearTerapia(models.TransientModel):
    _name = 'psicologia.crear.terapia.wizard'
    _description = 'Crear Terapia para Paciente'

    paciente_id = fields.Many2one('psicologia.paciente', string="Paciente", required=True)
    psicologo_ids = fields.Many2many('psicologia.psicologo', string="Psicólogos")
    fecha = fields.Date(string="Fecha de inicio", required=True, default=fields.Date.today)

    def action_crear_terapia(self):
        if not self.psicologo_ids:
            raise ValidationError("Debe seleccionarse al menos un psicólogo.")
        
        terapia = self.env['psicologia.terapia'].create({
            'paciente_id': self.paciente_id.id,
            'psicologo_ids': [(6, 0, self.psicologo_ids.ids)],
            'fecha': self.fecha,
        })
        return {
            'name': 'Nueva Terapia',
            'type': 'ir.actions.act_window',
            'res_model': 'psicologia.terapia',
            'view_mode': 'form',
            'res_id': terapia.id,
            'target': 'current',
        }
