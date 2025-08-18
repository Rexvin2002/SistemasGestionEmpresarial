# -*- coding: utf-8 -*-

# from odoo import models, fields, api

from odoo import models, fields, api
from datetime import timedelta 
from odoo.exceptions import UserError
from datetime import date
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo import _

class Continente(models.Model):
    _name = 'gestion_zoo.continente'
    _description = 'Continentes del zoo'

    name = fields.Char(string='Nombre:', required=True)
    especie_ids = fields.One2many('gestion_zoo.especie', 'continent_ids', string='Especies')

    def boton_especies_por_continente(self):
        for record in self:
            cantidad_especies = len(record.especie_ids)
            raise UserError(f'Este continente tiene {cantidad_especies} especie(s) en el zoo.')

class Especie(models.Model):
    _name = 'gestion_zoo.especie'
    _description = 'Especies del zoológico'
    _order = 'public_attraction desc, name asc'

    name = fields.Char(string='Nombre:', required=True)
    continent_ids = fields.Many2many('gestion_zoo.continente', string='Continentes:')
    public_attraction = fields.Integer(string='Atracción para el público:', default=0, required=True, invisible=True)
    popularity = fields.Float(string='Popularidad:', compute='_compute_popularity', store=True)
    image = fields.Image(string='Imagen:')
    peligrosidad = fields.Selection(
        [(str(i), str(i)) for i in range(5)],
        string='Peligrosidad',
        default='0',
        required=True
    )
    total_continentes = fields.Integer(string='Total Continentes:', compute='_compute_total_continentes', store=True)
    is_dangerous = fields.Boolean(string="Es peligrosa:", compute="_compute_is_dangerous", store=True)
    is_low_popularity = fields.Boolean(string="Baja popularidad:", compute="_compute_is_low_popularity", store=True)

    _sql_constraints = [
        ('check_attraction_range', 'CHECK(public_attraction BETWEEN 0 AND 10)',
         'La atracción para el público debe estar entre 0 y 10.')
    ]
    
    expected_lifespan = fields.Integer(
        string='Esperanza de vida (años):',
        help='Tiempo promedio de vida esperado para esta especie'
    )
    diet_type = fields.Selection([
        ('carnivore', 'Carnívoro'),
        ('herbivore', 'Herbívoro'),
        ('omnivore', 'Omnívoro')
    ], string='Tipo de Dieta:', required=True, default='herbivore')
    conservation_status = fields.Selection([
        ('ex', 'Extinto'),
        ('ew', 'Extinto en Estado Silvestre'),
        ('cr', 'En Peligro Crítico'),
        ('en', 'En Peligro'),
        ('vu', 'Vulnerable'),
        ('nt', 'Casi Amenazado'),
        ('lc', 'Preocupación Menor')
    ], string='Estado de Conservación:', required=True, default='lc')

    diet_line_ids = fields.One2many('gestion_zoo.diet_line', 'especie_id', string='Líneas de Dieta Recomendada')

    @api.depends('continent_ids')
    def _compute_total_continentes(self):
        """Calcula el número total de continentes asociados a la especie."""
        for record in self:
            record.total_continentes = len(record.continent_ids)

    @api.depends('public_attraction')
    def _compute_popularity(self):
        """Calcula el porcentaje de popularidad basado en la atracción pública."""
        for record in self:
            record.popularity = record.public_attraction * 10  # Escala 0-10 a 0-100%

    @api.depends('peligrosidad')
    def _compute_is_dangerous(self):
        """Determina si la especie es peligrosa."""
        for record in self:
            record.is_dangerous = int(record.peligrosidad) >= 3

    @api.depends('public_attraction')
    def _compute_is_low_popularity(self):
        """Determina si la especie tiene baja popularidad."""
        for record in self:
            record.is_low_popularity = record.public_attraction < 5


    def increase_popularity(self):
        """Incrementa la popularidad en 1 punto."""
        for record in self:
            if record.public_attraction < 10:
                record.public_attraction += 1

    def decrease_popularity(self):
        """Reduce la popularidad en 1 punto."""
        for record in self:
            if record.public_attraction > 0:
                record.public_attraction -= 1

class Animal(models.Model):
    _name = 'gestion_zoo.animal'
    _description = 'Animales del zoológico'

    # Statebar
    state = fields.Selection([
        ('normal', 'Normal'),
        ('sick', 'Enfermo'),
        ('recovery', 'En recuperación')
    ], string="Estado", default='normal', tracking=True)

    # Información General
    name = fields.Char(string='Nombre:', required=True)
    species_id = fields.Many2one('gestion_zoo.especie', string='Especie:', required=True)
    habitat_id = fields.Many2one('gestion_zoo.habitaculo', string='Hábitat:', required=True)
    arrival_date = fields.Date(string='Fecha de llegada:', required=True)
    birth_date = fields.Date(string='Fecha de nacimiento:')
    born_in_zoo = fields.Boolean(
        string='Nacido en el zoológico:',
        compute='_compute_born_in_zoo',
        store=True
    )
    caretaker_id = fields.Many2one(
        related='habitat_id.caretaker_id',
        string='Cuidador responsable:',
        readonly=True
    )
    caretaker_phone = fields.Char(
        related='caretaker_id.phone',
        string='Teléfono del Cuidador:',
        readonly=True
    )

    # Historial Médico
    medical_history = fields.Text(
        string='Historial Médico:',
        help='Registro histórico de condiciones médicas y tratamientos'
    )
    medical_checkups = fields.One2many(
        'gestion_zoo.medical.checkup',
        'animal_id',
        string='Revisiones Médicas:'
    )

    # Historial Comida
    comida_registro_ids = fields.One2many('gestion_zoo.comida_registro', 'animal_id', string='Registros de Comida:')
    species_image = fields.Image(
        related='species_id.image',
        readonly=True
    )
    tipo_comida_id = fields.Many2one(
        'gestion_zoo.tipocomida',
        string='Tipo de comida:',
        help='Tipo de comida que consume el animal, por ejemplo: pienso, carne, gusanos, zanahorias.'
    )

    # Métodos para establecer los estados
    def set_sick(self):
        self.ensure_one()
        self.state = 'sick'
    def set_in_recovery(self):
        self.ensure_one()
        self.state = 'recovery'
    def set_normal(self):
        self.ensure_one()
        self.state = 'normal'
    
    # Método para calcular si el animal nació en el zoológico
    @api.depends('arrival_date', 'birth_date')
    def _compute_born_in_zoo(self):
        for record in self:
            record.born_in_zoo = False
            if record.birth_date and record.arrival_date:
                record.born_in_zoo = record.birth_date <= record.arrival_date

    # Método para validar las fechas de nacimiento y llegada
    @api.constrains('birth_date', 'arrival_date')
    def _check_birth_date(self):
        for record in self:
            if record.birth_date and record.arrival_date and record.birth_date > record.arrival_date:
                raise ValidationError(_('La fecha de nacimiento no puede ser posterior a la fecha de llegada.'))

    # Método para registrar la comida
    def registrar_comida(self, fecha, tipo_comida_id, cantidad):
        self.ensure_one()
        self.env['gestion_zoo.comida_registro'].create({
            'animal_id': self.id,
            'fecha': fecha,
            'tipo_comida_id': tipo_comida_id,
            'cantidad': cantidad,
        })

    # Comprueba si el hábitat esta vacío o no
    def check_habitat_status(self):
        """Verificar si el hábitat está vacío o lleno."""
        if self.habitat_id:
            # Contar el número de animales en el hábitat
            animal_count = self.habitat_id.animal_ids.search_count([])
            
            # Obtener el máximo de animales permitidos en el hábitat
            max_animals = self.habitat_id.max_animals

            # Comprobar si el hábitat está lleno
            if max_animals and animal_count >= max_animals:
                return 'full'  # El hábitat está lleno
            elif animal_count == 0:
                return 'empty'  # El hábitat está vacío
            else:
                return 'not_full'  # El hábitat no está lleno ni vacío
        return 'empty'  # Si no hay hábitat asignado, lo consideramos vacío

    # Método para registrar el cambio de hábitat
    @api.onchange('habitat_id')
    def _check_animal_limit_in_habitat(self):
        """Verificar el estado del hábitat cuando se cambia el hábitat del animal."""
        habitat_status = self.check_habitat_status()
        if habitat_status == 'full':
            raise ValidationError(_('El hábitat está lleno. No se puede asignar más animales.'))
        elif habitat_status == 'empty':
            # Si el hábitat está vacío, se podría mostrar un mensaje o realizar alguna acción adicional
            pass  # Aquí puedes agregar alguna lógica extra si lo necesitas

    # Método para crear una cría del animal en cuestión
    def create_cria(self):
        """Crear una nueva cría del animal actual"""
        self.ensure_one()
        
        # Verificar el estado del hábitat
        habitat_status = self.check_habitat_status()

        if habitat_status == 'full':
            raise ValidationError(_('El hábitat está lleno. No se puede crear una cría.'))
        elif habitat_status == 'empty':
            # Si el hábitat está vacío, podrías implementar alguna lógica especial para este caso
            pass  # Aquí puedes agregar alguna lógica extra si lo necesitas

        # Comprobar si el límite de animales en el hábitat se va a exceder
        if self.habitat_id:
            # Obtener el máximo de animales permitidos en el hábitat
            max_animals = self.habitat_id.max_animals

            # Contar el número de animales en el hábitat (incluyendo la cría)
            animal_count = self.habitat_id.animal_ids.search_count([])

            # Si el número de animales va a superar el límite, mostrar un warning
            if max_animals and animal_count >= max_animals:
                raise ValidationError(_('El número máximo de animales en este habitáculo ha sido alcanzado o excedido.'))

        # Crear los valores de la cría
        cria_values = {
            'name': f"Cría de {self.name}",
            'species_id': self.species_id.id,
            'habitat_id': self.habitat_id.id,
            'arrival_date': fields.Date.today(),
            'birth_date': fields.Date.today(),
            'state': 'normal',
            'tipo_comida_id': self.tipo_comida_id.id,
        }
        
        # Crear la cría y mostrar su formulario
        cria = self.create(cria_values)
        
        # Retornar una acción para abrir el formulario de la nueva cría
        return {
            'name': 'Nueva Cría',
            'type': 'ir.actions.act_window',
            'res_model': 'gestion_zoo.animal',
            'res_id': cria.id,
            'view_mode': 'form',
            'target': 'current',
        }





class Cuidador(models.Model):
    _name = 'gestion_zoo.cuidador'
    _description = 'Cuidador del zoo'

    name = fields.Char(string='Nombre:', required=True)
    phone = fields.Char(string='Teléfono Kevin:')
    estudios = fields.Selection([
        ('eso', 'ESO'),
        ('bachillerato', 'Bachillerato'),
        ('ciclo_grado_medio', 'Ciclo Grado Medio'),
        ('ciclo_grado_superior', 'Ciclo Grado Superior'),
        ('universitario', 'Universitario')
    ], string='Estudios de Kevin', required=True)
    titulo = fields.Char(
        string='Título de Kevin',
        compute='_compute_titulo',
        readonly=False,
        store=True,
    )
    hide_titulo = fields.Boolean(
        string='Ocultar Título de Kevin',
        compute='_compute_hide_titulo'
    )
    salario = fields.Float(
        string='Salario',
        compute='_compute_salario',
        store=True
    )

    caretaker_id = fields.Many2one('some.model', string='Caretaker')
    total_habitaculos = fields.Integer(
        string='Total Habitáculos Kevin',
        compute='_compute_total_habitaculos',
        store=True
    )
    animal_ids = fields.One2many(
        'gestion_zoo.animal',
        'caretaker_id',
        string='Animales bajo cuidado de Kevin'
    )

    # Habitáculos bajo cuidado
    habitaculo_ids = fields.One2many(
        'gestion_zoo.habitaculo',
        'caretaker_id',
        string='Habitáculos bajo cuidado'
    )
    habitaculo_names = fields.Char(
        string='Habitáculos bajo cuidado',
        compute='_compute_habitaculo_names',
        readonly=True
    )

    estado_laboral_id = fields.Many2one(
        'gestion_zoo.estado_laboral',
        string="Estado Laboral",
        default=lambda self: self._default_estado_laboral(),
        required=True,
    )

    # Método que calcula el total de habitáculos a cargo del cuidador
    @api.depends('habitaculo_ids')
    def _compute_total_habitaculos(self):
        for record in self:
            record.total_habitaculos = len(record.habitaculo_ids)


    # Método que devuelve el estado laboral con sequence más baja
    @api.model
    def _default_estado_laboral(self):
        return self.env['gestion_zoo.estado_laboral'].search([], order='order', limit=1)
    
    # Método que cambia al siguiente estado laboral basado en la secuencia
    def cambiar_estado(self):
        """Cambia el estado laboral al siguiente en orden"""
        estados = self.env['gestion_zoo.estado_laboral'].search([], order='order')
        estado_actual = estados.filtered(lambda e: e.id == self.estado_laboral_id.id)
        if estado_actual:
            index = estados.ids.index(estado_actual.id)
            if index + 1 < len(estados):
                self.estado_laboral_id = estados[index + 1]


    # Método para computar visibilidad y requerimiento del título
    @api.depends('estudios')
    def _compute_titulo(self):
        for record in self:
            if record.estudios in ['ciclo_grado_superior', 'universitario']:
                record.titulo = record.titulo or ''
            else:
                record.titulo = False

    # Método para comprobar el requerimiento del campo titulo
    @api.constrains('estudios', 'titulo')
    def _check_titulo_required(self):
        for record in self:
            if record.estudios in ['ciclo_grado_superior', 'universitario'] and not record.titulo:
                raise ValidationError(
                    'El título es obligatorio para estudios de Ciclo Grado Superior o Universitario.'
                )

    # Método controlar la visibilidad del campo titulo
    @api.depends('estudios')
    def _compute_hide_titulo(self):
        for record in self:
            record.hide_titulo = record.estudios not in ['ciclo_grado_superior', 'universitario']

    # Método que computa los nombres de los habitáculos a cargo del cuidador.
    @api.depends('animal_ids')
    def _compute_habitaculo_names(self):
        for record in self:
            habitaculos = record.env['gestion_zoo.habitaculo'].search([('caretaker_id', '=', record.id)])
            record.habitaculo_names = ', '.join(habitaculos.mapped('name'))




class Habitaculo(models.Model):
    _name = 'gestion_zoo.habitaculo'
    _description = 'Habitáculo del Zoológico'
    _order = 'surface desc'  # Ordenar por superficie de mayor a menor

    name = fields.Char(string='Nombre', required=True)
    zone = fields.Char(string='Zona', required=True)
    surface = fields.Float(string='Área (m²)', digits=(6, 2), required=True)
    habitat_type = fields.Selection([
        ('exterior', 'Exterior'),
        ('aviario', 'Aviario'),
        ('granja', 'Granja'),
        ('terrario', 'Terrario'),
        ('acuario', 'Acuario')
    ], string='Tipo de hábitat', required=True)
    cleaning_date = fields.Date(string='Última limpieza', default=fields.Date.today)
    days_since_cleaning = fields.Integer(
        string='Días de la última limpieza', compute='_compute_days_since_cleaning', store=False
    )
    next_cleaning_date = fields.Date(
        string='Próxima limpieza', compute='_compute_next_cleaning_date', store=True
    )
    cleaning_urgency = fields.Float(
        string='Urgencia de limpieza', compute='_compute_cleaning_urgency', store=False
    )
    caretaker_id = fields.Many2one(
        'gestion_zoo.cuidador', string='Cuidador responsable'
    )
    total_animals = fields.Integer(
        string='Total de Animales', compute='_compute_total_animals', store=False
    )
    animal_ids = fields.One2many(
        'gestion_zoo.animal', 'habitat_id', string='Animales'
    )
    is_cleaning_due = fields.Boolean(
        string='¿Limpieza vencida?', compute='_compute_is_cleaning_due', store=False
    )

    # Campo añadido para el máximo número de animales
    max_animals = fields.Integer(
        string='Máximo de Animales', required=True, default=10
    )

    maintenance_cost = fields.Float(
        string='Coste de Mantenimiento Mensual',
        help='Coste mensual estimado para el mantenimiento del hábitat',
        digits=(10, 2)
    )

    def open_add_food_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Añadir Alimentos a Dieta',
            'res_model': 'gestion_zoo.add_food_wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    def open_add_continent_wizard(self):
        """Abre el wizard para añadir un continente a las especies seleccionadas en este habitáculo."""
        self.ensure_one()  # Asegurarse de que solo se seleccione un registro
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Continent to Species',
            'res_model': 'gestion_zoo.add_continent_wizard',  # El modelo de tu wizard
            'view_mode': 'form',
            'view_id': self.env.ref('gestion_zoo.view_add_continent_wizard_form').id,
            'target': 'new',
            'context': {
                'default_habitaculo_id': self.id,  # Pasa el ID del habitáculo al wizard
            },
        }

    def open_eliminar_alimento_wizard(self):
        # Retorna la acción que abre el wizard
        return {
            'type': 'ir.actions.act_window',
            'name': 'Eliminar Alimentos de Dieta',
            'res_model': 'gestion_zoo.eliminar_alimento_wizard',
            'view_mode': 'form',
            'target': 'new',
        }


    @api.constrains('total_animals')
    def _check_max_animals(self):
        for record in self:
            if record.total_animals > record.max_animals:
                raise ValidationError(
                    f"El número de animales no puede superar el máximo permitido de {record.max_animals}."
                )

    @api.depends('next_cleaning_date')
    def _compute_is_cleaning_due(self):
        for record in self:
            record.is_cleaning_due = record.next_cleaning_date and record.next_cleaning_date < fields.Date.today()

    @api.depends('animal_ids')
    def _compute_total_animals(self):
        for record in self:
            record.total_animals = len(record.animal_ids)

    @api.depends('cleaning_date')
    def _compute_days_since_cleaning(self):
        for record in self:
            if record.cleaning_date:
                record.days_since_cleaning = (fields.Date.today() - record.cleaning_date).days
            else:
                record.days_since_cleaning = 0

    @api.depends('cleaning_date', 'habitat_type')
    def _compute_next_cleaning_date(self):
        cleaning_intervals = {
            'exterior': 30,
            'aviario': 15,
            'granja': 10,
            'terrario': 20,
            'acuario': 7,
        }
        for record in self:
            interval = cleaning_intervals.get(record.habitat_type, 7)
            record.next_cleaning_date = record.cleaning_date + timedelta(days=interval) if record.cleaning_date else None

    @api.depends('cleaning_date', 'next_cleaning_date')
    def _compute_cleaning_urgency(self):
        for record in self:
            if record.cleaning_date and record.next_cleaning_date:
                total_days = (record.next_cleaning_date - record.cleaning_date).days
                remaining_days = (record.next_cleaning_date - fields.Date.today()).days
                if total_days > 0 and remaining_days >= 0:
                    record.cleaning_urgency = (1 - remaining_days / total_days) * 100
                elif remaining_days < 0:
                    record.cleaning_urgency = 100.0
                else:
                    record.cleaning_urgency = 0.0
            else:
                record.cleaning_urgency = 0.0

    def mark_cleaned_today(self):
        self.cleaning_date = fields.Date.today()
        self.invalidate_cache()
        return True

    def action_confirm_cleaning(self):
        for record in self:
            return record.write({
                'cleaning_date': fields.Date.today()
            })

    @api.constrains('surface')
    def _check_surface(self):
        for record in self:
            if record.surface <= 0:
                raise ValidationError("La superficie debe ser mayor que 0.")

class MedicalCheckup(models.Model):
    _name = 'gestion_zoo.medical.checkup'
    _description = 'Revisiones Médicas de Animales'
    _order = 'date desc'

    animal_id = fields.Many2one(
        'gestion_zoo.animal',
        string='Animal',
        required=True
    )
    date = fields.Date(
        string='Fecha de Revisión',
        required=True,
        default=fields.Date.today
    )
    veterinarian = fields.Char(
        string='Veterinario',
        required=True
    )
    diagnosis = fields.Text(
        string='Diagnóstico',
        required=True
    )
    treatment = fields.Text(
        string='Tratamiento Prescrito'
    )
    next_checkup = fields.Date(
        string='Próxima Revisión'
    )

class TipoComidaAnimales(models.Model):
    _name = 'gestion_zoo.tipocomida'
    _description = 'Tipos de comida para los animales'

    name = fields.Char(string='Nombre', required=True, help='Nombre del tipo de comida, por ejemplo: pienso, carne, gusanos, zanahorias.')

class DietLine(models.Model):
    _name = 'gestion_zoo.diet_line'
    _description = 'Línea de Dieta Recomendada'

    especie_id = fields.Many2one('gestion_zoo.especie', string='Especie', required=True, ondelete='cascade')
    food_id = fields.Many2one('gestion_zoo.tipocomida', string='Comida', required=True)
    quantity_kg = fields.Float(string='Kg', required=True)

class CambiarHabitaculoWizard(models.TransientModel):
    _name = 'gestion_zoo.cambiar_habitaculo_wizard'
    _description = 'Wizard para cambiar el habitáculo de los animales'

    species_id = fields.Many2one('gestion_zoo.especie', string='Especie', required=True)
    habitat_origen_id = fields.Many2one('gestion_zoo.habitaculo', string='Habitáculo de Origen', required=True)
    habitat_destino_id = fields.Many2one('gestion_zoo.habitaculo', string='Habitáculo de Destino', required=True)

    def cambiar_habitaculo(self):
        # Buscar los animales de la especie seleccionada que estén en el habitáculo de origen
        animals_to_move = self.env['gestion_zoo.animal'].search([
            ('species_id', '=', self.species_id.id),
            ('habitat_id', '=', self.habitat_origen_id.id)
        ])

        # Si no hay animales en el habitáculo de origen, mostrar un mensaje de error
        if not animals_to_move:
            raise ValidationError(_('No hay animales en el habitáculo de origen para la especie seleccionada.'))

        # Cambiar el habitáculo de todos los animales seleccionados
        for animal in animals_to_move:
            animal.habitat_id = self.habitat_destino_id

        return {'type': 'ir.actions.act_window_close'}
    
class EliminarAlimentoWizard(models.TransientModel):
    _name = 'gestion_zoo.eliminar_alimento_wizard'
    _description = 'Wizard para eliminar alimento de dietas de especies'

    # Campos para seleccionar los alimentos y las especies
    food_ids = fields.Many2many(
        'gestion_zoo.tipocomida', 
        string='Alimentos', 
        required=True
    )
    species_ids = fields.Many2many(
        'gestion_zoo.especie', 
        string='Especies', 
        required=True
    )

    def action_remove_food_from_diet(self):
        """Eliminar los alimentos seleccionados de las dietas de las especies seleccionadas"""
        for specie in self.species_ids:
            # Buscar todas las líneas de dieta para la especie
            diet_lines = self.env['gestion_zoo.diet_line'].search([
                ('especie_id', '=', specie.id),
                ('food_id', 'in', self.food_ids.ids)  # Filtrar por los alimentos seleccionados
            ])
            # Eliminar las líneas de dieta que coinciden con los alimentos seleccionados
            diet_lines.unlink()

        return {'type': 'ir.actions.act_window_close'}

class AddContinentWizard(models.TransientModel):
    _name = 'gestion_zoo.add_continent_wizard'
    _description = 'Wizard para agregar continente a las especies seleccionadas'

    
    continent_ids = fields.Many2many('gestion_zoo.continent', string="Continentes")
    species_ids = fields.Many2many('gestion_zoo.especie', string='Especies', required=True)

    def action_add_continent(self):
        """Asocia el continente seleccionado a las especies seleccionadas"""
        for species in self.species_ids:
            species.continent_id = self.continent_id
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        """Cierra el wizard sin hacer cambios"""
        return {'type': 'ir.actions.act_window_close'}

class AddAlimentoWizard(models.TransientModel):
    _name = 'gestion_zoo.add_food_wizard'
    _description = 'Wizard para añadir alimento a las dietas de especies'

    # Campos para seleccionar los alimentos, especies y la cantidad
    food_ids = fields.Many2many(
        'gestion_zoo.tipocomida', 
        string='Alimentos', 
        required=True
    )
    species_ids = fields.Many2many(
        'gestion_zoo.especie', 
        string='Especies', 
        required=True
    )
    quantity = fields.Float(
        string='Kg',
        required=True,
        help="Cantidad de alimento que se añadirá a las dietas"
    )

    def action_add_food_to_diet(self):
        """Añadir los alimentos seleccionados a las dietas de las especies seleccionadas"""
        for specie in self.species_ids:
            # Buscar todas las líneas de dieta para la especie
            diet_lines = self.env['gestion_zoo.diet_line'].search([ 
                ('especie_id', '=', specie.id),
                ('food_id', 'in', self.food_ids.ids)  # Filtrar por los alimentos seleccionados
            ])
            # Añadir los alimentos con la cantidad seleccionada a las dietas
            for food in self.food_ids:
                # Crear una nueva línea de dieta con la cantidad indicada
                self.env['gestion_zoo.diet_line'].create({
                    'especie_id': specie.id,
                    'food_id': food.id,
                    'quantity_kg': self.quantity  # Cambiar 'quantity' a 'quantity_kg'
                })

        return {'type': 'ir.actions.act_window_close'}

class AnimalGroupWizard(models.TransientModel):
    _name = 'gestion_zoo.animal.group.wizard'
    _description = 'Asistente para crear grupos de animales'

    name = fields.Char(string='Nombre base', required=True, help='Se añadirá un número al final de este nombre')
    species_id = fields.Many2one('gestion_zoo.especie', string='Especie', required=True)
    habitat_id = fields.Many2one('gestion_zoo.habitaculo', string='Hábitat', required=True)
    number_of_animals = fields.Integer(string='Número de animales', required=True, default=1)
    tipo_comida_id = fields.Many2one('gestion_zoo.tipocomida', string='Tipo de comida', required=True)
    state = fields.Selection([
        ('normal', 'Normal'),
        ('sick', 'Enfermo'),
        ('recovery', 'En recuperación')
    ], string="Estado", default='normal')

    @api.constrains('number_of_animals')
    def _check_number_of_animals(self):
        for record in self:
            if record.number_of_animals <= 0:
                raise ValidationError(_('El número de animales debe ser mayor que 0'))

    def create_animal_group(self):
        self.ensure_one()
        Animal = self.env['gestion_zoo.animal']
        
        # Comprobar el límite de animales en el hábitat
        max_animals = self.habitat_id.max_animals
        current_count = self.habitat_id.animal_ids.search_count([])
        
        if max_animals and (current_count + self.number_of_animals) > max_animals:
            raise ValidationError(_(
                'No hay suficiente espacio en el hábitat. '
                'Capacidad máxima: %d, Actuales: %d, Intentando añadir: %d'
            ) % (max_animals, current_count, self.number_of_animals))

        # Crear los animales
        animal_ids = []
        for i in range(self.number_of_animals):
            animal = Animal.create({
                'name': f"{self.name} {i + 1}",
                'species_id': self.species_id.id,
                'habitat_id': self.habitat_id.id,
                'arrival_date': fields.Date.today(),
                'state': self.state,
                'tipo_comida_id': self.tipo_comida_id.id,
            })
            animal_ids.append(animal.id)

        # Retornar una acción para mostrar los animales creados
        return {
            'name': 'Animales Creados',
            'type': 'ir.actions.act_window',
            'res_model': 'gestion_zoo.animal',
            'domain': [('id', 'in', animal_ids)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
    
class ComidaRegistro(models.Model):
    _name = 'gestion_zoo.comida_registro'
    _description = 'Registro de comida consumida por los animales'

    animal_id = fields.Many2one('gestion_zoo.animal', string='Animal', required=True)
    fecha = fields.Date(string='Fecha', required=True)
    tipo_comida_id = fields.Many2one('gestion_zoo.tipocomida', string='Tipo de comida', required=True)
    cantidad = fields.Float(string='Cantidad (kg)', required=True)

class FeedAnimalsWizard(models.TransientModel):
    _name = 'gestion_zoo.feed.animals.wizard'
    _description = 'Wizard para registrar comida para los animales'

    habitaculo_id = fields.Many2one('gestion_zoo.habitaculo', string="Habitáculo", required=True)
    date_start = fields.Date(string="Fecha de Inicio", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Fecha de Fin", required=True, default=fields.Date.today)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_end < record.date_start:
                raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
            
            # Verificar que el rango de fechas no sea superior a 31 días
            delta = record.date_end - record.date_start
            if delta.days > 31:
                raise ValidationError("El rango de fechas no puede ser superior a 31 días.")
            
            # Verificar que las fechas no sean futuras
            if record.date_end > fields.Date.today():
                raise ValidationError("No se pueden registrar comidas para fechas futuras.")

    def action_register_food(self):
        self.ensure_one()
        ComidaRegistro = self.env['gestion_zoo.comida_registro']
        
        # Buscar animales en el habitáculo
        animales = self.env['gestion_zoo.animal'].search([
            ('habitat_id', '=', self.habitaculo_id.id)
        ])
        
        if not animales:
            raise ValidationError(f"No se encontraron animales en el habitáculo {self.habitaculo_id.name}.")

        registros_creados = 0
        current_date = self.date_start
        
        while current_date <= self.date_end:
            for animal in animales:
                # Verificar si ya existe un registro para esta fecha
                existe_registro = ComidaRegistro.search_count([
                    ('animal_id', '=', animal.id),
                    ('fecha', '=', current_date)
                ])
                
                if existe_registro == 0:
                    # Obtener el tipo de comida del animal
                    if not animal.tipo_comida_id:
                        raise ValidationError(
                            f"El animal {animal.name} no tiene un tipo de comida asignado."
                        )
                    
                    # Crear registro de comida
                    ComidaRegistro.create({
                        'animal_id': animal.id,
                        'fecha': current_date,
                        'tipo_comida_id': animal.tipo_comida_id.id,
                        'cantidad': 1.0,  # Cantidad por defecto, ajustar según necesidades
                    })
                    registros_creados += 1
            
            current_date += timedelta(days=1)

        # Mensaje de éxito con resumen
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Registros de alimentación creados',
                'message': f'Se han creado {registros_creados} registros de alimentación.',
                'type': 'success',
                'sticky': False,
            }
        }
    
class EstadoLaboral(models.Model):
    _name = 'gestion_zoo.estado_laboral'
    _description = 'Estados laborales de los empleados'
    _order = 'order'

    name = fields.Char(string="Estado Laboral", required=True)
    order = fields.Integer(string="Orden", default=1)
