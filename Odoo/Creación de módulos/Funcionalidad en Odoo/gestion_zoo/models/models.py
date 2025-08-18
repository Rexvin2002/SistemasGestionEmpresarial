# -*- coding: utf-8 -*-

# from odoo import models, fields, api

from odoo import models, fields, api
from datetime import timedelta 
from odoo.exceptions import UserError
from datetime import date
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo import _
import logging

_logger = logging.getLogger(__name__)

class Continente(models.Model):
    _name = 'gestion_zoo.continente'
    _description = 'Continentes del zoo'

    name = fields.Char(string='Nombre', required=True)
    especie_ids = fields.Many2many('gestion_zoo.especie', string='Especies')
    empresa_ids = fields.Many2many('gestion_zoo.empresa', string='Empresa')

    # Calcula el número total de especies por continente
    def boton_especies_por_continente(self):
        mensajes = []
        for record in self:
            cantidad_especies = len(record.especie_ids)
            mensajes.append(f'El continente "{record.name}" tiene {cantidad_especies} especie(s).')
        # Muestra el mensaje en un cuadro de alerta
        raise UserError('\n'.join(mensajes))
    
    # Método para abrir el wizard
    def open_wizard_empresas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Empresas por Continente',
            'res_model': 'gestion_zoo.wizard_empresas_por_continente',
            'view_mode': 'form',
            'target': 'new',  # Abre en una ventana modal
            'context': {
                'default_continente_id': self.id,  # Pasa el continente seleccionado al wizard
            }
        }

    # Método para abrir el wizard de locales por continente
    def open_wizard_locales(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Locales por Continente',
            'res_model': 'gestion_zoo.wizard_locales_por_continente',
            'view_mode': 'form',
            'target': 'new',  # Abre en una ventana modal
            'context': {
                'default_continente_id': self.id,  # Pasa el continente seleccionado al wizard
            }
        }
    


class Especie(models.Model):
    _name = 'gestion_zoo.especie'
    _description = 'Especies del zoológico'
    _order = 'public_attraction desc, name asc'

    image = fields.Image(string='Imagen')
    name = fields.Char(string='Nombre', required=True)
    continent_ids = fields.Many2many('gestion_zoo.continente', string='Continentes')
    total_continentes = fields.Integer(string='Total Continentes', compute='_compute_total_continentes', store=True)
    expected_lifespan = fields.Integer(
        string='Esperanza de vida (años):',
        help='Tiempo promedio de vida esperado para esta especie'
    )
    diet_type = fields.Selection([
        ('carnivore', 'Carnívoro'),
        ('herbivore', 'Herbívoro'),
        ('omnivore', 'Omnívoro')
    ], string='Tipo de Dieta:', required=True, default='herbivore')
    diet_line_ids = fields.One2many('gestion_zoo.diet_line', 'especie_id', string='Líneas de Dieta Recomendada')
    conservation_status = fields.Selection([
        ('ex', 'Extinto'),
        ('ew', 'Extinto en Estado Silvestre'),
        ('cr', 'En Peligro Crítico'),
        ('en', 'En Peligro'),
        ('vu', 'Vulnerable'),
        ('nt', 'Casi Amenazado'),
        ('lc', 'Preocupación Menor')
    ], string='Estado de Conservación:', required=True, default='lc')
    peligrosidad = fields.Selection(
        [(str(i), str(i)) for i in range(5)],
        string='Peligrosidad',
        default='0',
        required=True
    )
    popularity = fields.Float(string='Popularidad', compute='_compute_popularity', store=True)

    public_attraction = fields.Integer(string='Atracción para el público', default=0, required=True, invisible=True)
    is_dangerous = fields.Boolean(string="Es peligrosa", compute="_compute_is_dangerous", store=True)
    is_low_popularity = fields.Boolean(string="Baja popularidad", compute="_compute_is_low_popularity", store=True)
    _sql_constraints = [
        ('check_attraction_range', 'CHECK(public_attraction BETWEEN 0 AND 10)',
         'La atracción para el público debe estar entre 0 y 10.')
    ]
    
    # Calcula el número total de continentes asociados a la especie.
    @api.depends('continent_ids')
    def _compute_total_continentes(self):
        for record in self:
            record.total_continentes = len(record.continent_ids)

    # Calcula el porcentaje de popularidad basado en la atracción pública.
    @api.depends('public_attraction')
    def _compute_popularity(self):
        for record in self:
            record.popularity = record.public_attraction * 10  # Escala 0-10 a 0-100%

    # Determina si la especie es peligrosa.
    @api.depends('peligrosidad')
    def _compute_is_dangerous(self):
        for record in self:
            record.is_dangerous = int(record.peligrosidad) >= 3

    # Determina si la especie tiene baja popularidad.
    @api.depends('public_attraction')
    def _compute_is_low_popularity(self):
        for record in self:
            record.is_low_popularity = record.public_attraction < 5

    # Incrementa la popularidad en 1 punto.
    def increase_popularity(self):
        for record in self:
            if record.public_attraction < 10:
                record.public_attraction += 1

    # Reduce la popularidad en 1 punto.
    def decrease_popularity(self):
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

    # Información General
    species_image = fields.Image(
        related='species_id.image',
        readonly=True
    )
    name = fields.Char(string='Nombre', required=True)
    species_id = fields.Many2one('gestion_zoo.especie', string='Especie', required=True)
    habitat_id = fields.Many2one('gestion_zoo.habitaculo', string='Hábitat', required=True)
    arrival_date = fields.Date(string='Fecha de llegada', required=True)
    birth_date = fields.Date(string='Fecha de nacimiento')
    born_in_zoo = fields.Boolean(
        string='Nacido en el zoológico',
        compute='_compute_born_in_zoo',
        store=True
    )
    caretaker_id = fields.Many2one(
        related='habitat_id.caretaker_id',
        string='Cuidador responsable',
        readonly=True
    )
    caretaker_phone = fields.Char(
        related='caretaker_id.phone',
        string='Teléfono del Cuidador',
        readonly=True
    )

    # Historial Médico
    medical_history = fields.Text(
        string='Historial Médico',
        help='Registro histórico de condiciones médicas y tratamientos'
    )
    medical_checkups = fields.One2many(
        'gestion_zoo.medical.checkup',
        'animal_id',
        string='Revisiones Médicas'
    )

    # Historial Comida
    comida_registro_ids = fields.One2many('gestion_zoo.comida_registro', 'animal_id', string='Registros de Comida')
    tipo_comida_id = fields.Many2one(
        'gestion_zoo.tipocomida',
        string='Tipo de comida',
        required=True,
        help='Tipo de comida que consume el animal, por ejemplo: pienso, carne, gusanos, zanahorias.'
    )


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
    

    # Devuelve la cantidad de registros en el conjunto actual.
    def read_count(self, domain=None):
        """Devuelve la cantidad de registros que cumplen con el dominio especificado."""
        domain = domain or []  # Asegurarse de que el dominio sea una lista
        return self.search_count(domain)

    # Verificar si el hábitat está vacío o lleno.
    def check_habitat_status(self):
        """Verifica el estado actual del hábitat con logging detallado."""
        if self.habitat_id:
            # Obtener conteos de diferentes maneras para depurar
            direct_count = len(self.habitat_id.animal_ids)
            computed_total = self.habitat_id.total_animals
            max_animals = self.habitat_id.max_animals
            
            # Log para depuración
            _logger.info(f"""
            Diagnóstico de Hábitat:
            - ID del Hábitat: {self.habitat_id.id}
            - Nombre del Hábitat: {self.habitat_id.name}
            - Conteo directo de animales: {direct_count}
            - Total computado de animales: {computed_total}
            - Máximo permitido: {max_animals}
            - IDs de animales actuales: {self.habitat_id.animal_ids.ids}
            """)
            
            if direct_count < max_animals:
                return 'not_full'
            elif direct_count >= max_animals:
                return 'full'
            return 'not_full'
        return 'empty'
    
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

    @api.constrains('habitat_id')
    def _check_single_habitat(self):
        """Impide que un animal esté asignado a múltiples hábitats."""
        for animal in self:
            if animal.habitat_id and len(animal.habitat_id.animal_ids) > animal.habitat_id.max_animals:
                raise ValidationError(_(
                    'El hábitat %s ha alcanzado su capacidad máxima.' % animal.habitat_id.name
                ))

    # Crear una nueva cría del animal actual
    def create_cria(self):
        self.ensure_one()
        
        if not self.habitat_id:
            raise ValidationError(_('El animal debe tener un hábitat asignado para crear una cría.'))
        
        # Log del estado actual antes de crear la cría
        _logger.info(f"""
        Intento de creación de cría:
        - Animal padre: {self.name} (ID: {self.id})
        - Hábitat: {self.habitat_id.name} (ID: {self.habitat_id.id})
        - Animales actuales en hábitat: {len(self.habitat_id.animal_ids)}
        - Máximo permitido: {self.habitat_id.max_animals}
        - Estado del hábitat: {self.check_habitat_status()}
        """)
        
        habitat_status = self.check_habitat_status()
        if habitat_status == 'full':
            raise ValidationError(_(
                f'El hábitat está lleno.\n'
                f'Animales actuales: {len(self.habitat_id.animal_ids)}\n'
                f'Máximo permitido: {self.habitat_id.max_animals}\n'
                f'IDs de animales en el hábitat: {self.habitat_id.animal_ids.ids}'
            ))
        
        # Crear los valores de la cría
        cria_values = {
            'name': f"Cría de {self.name}",
            'species_id': self.species_id.id,
            'habitat_id': self.habitat_id.id,
            'arrival_date': fields.Date.today(),
            'birth_date': fields.Date.today(),
            'state': 'normal',
            'tipo_comida_id': self.tipo_comida_id.id if self.tipo_comida_id else False,
        }
        
        # Crear la cría
        cria = self.create(cria_values)
        
        # Log después de la creación
        _logger.info(f"""
        Cría creada exitosamente:
        - ID de la cría: {cria.id}
        - Nombre de la cría: {cria.name}
        - Nuevo total de animales en hábitat: {len(self.habitat_id.animal_ids)}
        """)
        
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

    # Statusbar de estados laborales
    estado_laboral_id = fields.Many2one(
        'gestion_zoo.estado_laboral',
        string="Estado Laboral",
        default=lambda self: self._default_estado_laboral(),
        required=True,
    )
    
    # Información Básica
    name = fields.Char(string='Nombre', required=True)
    phone = fields.Char(string='Teléfono Kevin')
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

    # Animales bajo cuidado
    animal_ids = fields.One2many(
        'gestion_zoo.animal',
        'caretaker_id',
        string='Animales bajo cuidado de Kevin'
    )
    caretaker_id = fields.Many2one('some.model', string='Caretaker')

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
    total_habitaculos = fields.Integer(
        string='Total Habitáculos Kevin',
        compute='_compute_total_habitaculos',
        store=True
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
    
    # Cambia el estado laboral al siguiente en orden
    def cambiar_estado(self):
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
    
    # Método para computar el salario
    @api.depends('estado_laboral_id.salary_base', 'estudios')
    def _compute_salario(self):
        for record in self:
            salario_base = record.estado_laboral_id.salary_base
            aumento = 0
            if record.estudios == 'eso':
                aumento = 0.10  # 10% de aumento
            elif record.estudios in ['ciclo_grado_superior', 'universitario']:
                aumento = 0.50  # 50% de aumento
            record.salario = salario_base * (1 + aumento)

    # Método que devuelve el estado laboral con sequence más baja
    @api.model
    def _default_estado_laboral(self):
        return self.env['gestion_zoo.estado_laboral'].search([], order='order', limit=1)

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
    maintenance_cost = fields.Float(
        string='Coste de Mantenimiento Mensual',
        help='Coste mensual estimado para el mantenimiento del hábitat',
        digits=(10, 2)
    )
    caretaker_id = fields.Many2one(
        'gestion_zoo.cuidador', string='Cuidador responsable'
    )
    animal_ids = fields.One2many(
        'gestion_zoo.animal', 'habitat_id', string='Animales'
    )
    max_animals = fields.Integer(
        string='Máximo de Animales', required=True, default=10
    )
    total_animals = fields.Integer(
        string='Total de Animales', compute='_compute_total_animals', store=False
    )
    cleaning_date = fields.Date(string='Última limpieza', default=fields.Date.today)
    next_cleaning_date = fields.Date(
        string='Próxima limpieza', compute='_compute_next_cleaning_date', store=True
    )
    cleaning_urgency = fields.Float(
        string='Urgencia de limpieza', compute='_compute_cleaning_urgency', store=False
    )

    is_cleaning_due = fields.Boolean(
        string='¿Limpieza vencida?', compute='_compute_is_cleaning_due', store=False
    )
    days_since_cleaning = fields.Integer(
        string='Días de la última limpieza', compute='_compute_days_since_cleaning', store=False
    )

    # Comprueba que la superficie es mayor que zero
    @api.constrains('surface')
    def _check_surface(self):
        for record in self:
            if record.surface <= 0:
                raise ValidationError("La superficie debe ser mayor que 0.")


    # Método para comprobar si el habitáculo está lleno
    def is_full(self):
        """Check if the habitat is full."""
        for record in self:
            if record.total_animals >= record.max_animals:
                return True
        return False

    # Restricción para validar que no se supere el máximo de animales permitidos
    @api.constrains('total_animals')
    def _check_max_animals(self):
        for record in self:
            if record.is_full():
                raise ValidationError(
                    f"El número de animales no puede superar el máximo permitido de {record.max_animals}."
                )
            
    # Calcula número total de animales
    @api.depends('animal_ids')
    def _compute_total_animals(self):
        for record in self:
            total = len(record.animal_ids)
            _logger.info(f"""
            Computando total_animals para hábitat {record.name} (ID: {record.id}):
            - Conteo directo: {total}
            - IDs de animales: {record.animal_ids.ids}
            """)
            record.total_animals = total

    @api.constrains('animal_ids')
    def _check_unique_habitat(self):
        """Asegura que los animales no estén asignados a múltiples hábitats."""
        for habitat in self:
            animal_ids = habitat.animal_ids.mapped('id')
            overlapping_animals = self.env['gestion_zoo.animal'].search([
                ('id', 'in', animal_ids),
                ('habitat_id', '!=', habitat.id)
            ])
            if overlapping_animals:
                raise ValidationError(_(
                    'Los siguientes animales ya están asignados a otro hábitat: %s'
                ) % ', '.join(overlapping_animals.mapped('name')))



    # Calcula si es necesario limpiar
    @api.depends('next_cleaning_date')
    def _compute_is_cleaning_due(self):
        for record in self:
            record.is_cleaning_due = record.next_cleaning_date and record.next_cleaning_date < fields.Date.today()

    # Calcula los dias desde la última limpieza
    @api.depends('cleaning_date')
    def _compute_days_since_cleaning(self):
        for record in self:
            if record.cleaning_date:
                record.days_since_cleaning = (fields.Date.today() - record.cleaning_date).days
            else:
                record.days_since_cleaning = 0

    # Calcula la siguiente fecha para limpiar
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

    # Calcula cuando se considera urgente la limpieza
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

    
    # Función del botón para marcar que el habitaculo esta limpio
    def action_confirm_cleaning(self):
        for record in self:
            return record.write({
                'cleaning_date': fields.Date.today()
            })

    # Cambia las fechas de limpiado tras pulsar el botón de marcar como limpio
    def mark_cleaned_today(self):
        self.cleaning_date = fields.Date.today()
        self.invalidate_cache()
        return True


    # Wizard para añadir comida 
    def open_add_food_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Añadir Alimentos a Dieta',
            'res_model': 'gestion_zoo.add_food_wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    # Wizard para añadir un continente a las especies seleccionadas en este habitáculo.
    def open_add_continent_wizard(self):
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

    # Wizard para eliminar un alimento
    def open_eliminar_alimento_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Eliminar Alimentos de Dieta',
            'res_model': 'gestion_zoo.eliminar_alimento_wizard',
            'view_mode': 'form',
            'target': 'new',
        }

class EstadoLaboral(models.Model):
    _name = 'gestion_zoo.estado_laboral'
    _description = 'Estados laborales de los empleados'
    _order = 'order'

    name = fields.Char(string="Estado Laboral", required=True)
    order = fields.Integer(string="Orden", default=1)
    salary_base = fields.Float(string='Salario Base', help="Salario base asociado a este estado laboral")
    average_salary = fields.Float(
        string="Average Salary",
        compute="_compute_average_salary",
        store=True
    )

    # Botón para calcular la masa salarial total
    def calcular_masa_salarial(self):
        # Obtener todos los cuidadores
        cuidadores = self.env['gestion_zoo.cuidador'].search([])
        # Calcular la suma de los salarios
        masa_salarial = sum(cuidador.salario for cuidador in cuidadores)
        # Mostrar un mensaje con el resultado
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Masa Salarial Total',
                'message': f'La masa salarial total es: {masa_salarial:.2f} €',
                'type': 'info',  # 'info', 'warning', 'danger'
                'sticky': False,
            }
        }
    
    @api.depends('salary_base')
    def _compute_average_salary(self):
        for record in self:
            # Obtener cuidadores que tienen este estado laboral
            cuidadores = self.env['gestion_zoo.cuidador'].search([('estado_laboral_id', '=', record.id)])
            # Calcular la media de salarios
            if cuidadores:
                record.average_salary = sum(cuidador.salario for cuidador in cuidadores) / len(cuidadores)
            else:
                record.average_salary = 0.0


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

    @api.constrains('name')
    def _check_unique_name(self):
        """
        Valida que no haya duplicados en el nombre de los tipos de comida.
        """
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError(f"El tipo de comida '{record.name}' ya existe.")


class DietLine(models.Model):
    _name = 'gestion_zoo.diet_line'
    _description = 'Líneas de Dieta Recomendada'

    especie_id = fields.Many2one('gestion_zoo.especie', string='Especie', required=True)
    tipo_comida_id = fields.Many2one('gestion_zoo.tipocomida', string='Tipo de Comida', required=True)
    cantidad = fields.Float(string='Cantidad Recomendada (kg)', required=True)

    @api.constrains('quantity_kg')
    def _check_quantity_kg(self):
        """
        Verifica que la cantidad recomendada de comida no sea 0.
        """
        for record in self:
            if record.cantidad <= 0:
                raise ValidationError(( 
                    "La cantidad recomendada de comida para la especie '{especie}' y el tipo de comida '{comida}' "
                    "debe ser mayor que 0 kg."
                ).format(
                    especie=record.especie_id.name or "desconocida",
                    comida=record.tipo_comida_id.name or "desconocido"
                ))


class ComidaRegistro(models.Model):
    _name = 'gestion_zoo.comida_registro'
    _description = 'Registro de comida consumida por los animales'

    animal_id = fields.Many2one('gestion_zoo.animal', string='Animal', required=True, readonly=True)
    fecha = fields.Date(string='Fecha', required=True)
    tipo_comida_id = fields.Many2one('gestion_zoo.tipocomida', string='Tipo de comida', required=True)
    cantidad = fields.Float(string='Cantidad (kg)', required=True)
    
    @api.constrains('cantidad')
    def _check_cantidad(self):
        for record in self:
            if record.cantidad <= 0:
                raise ValidationError("La cantidad de comida debe ser mayor que 0.")



class CambiarHabitaculoWizard(models.TransientModel):
    _name = 'gestion_zoo.cambiar_habitaculo_wizard'
    _description = 'Wizard para cambiar el habitáculo de los animales'

    species_id = fields.Many2one('gestion_zoo.especie', string='Especie', required=True)
    habitat_origen_id = fields.Many2one('gestion_zoo.habitaculo', string='Habitáculo de Origen', required=True)
    habitat_destino_id = fields.Many2one('gestion_zoo.habitaculo', string='Habitáculo de Destino', required=True)

    def cambiar_habitaculo(self):
        # Verificar si el habitáculo de destino está lleno
        if self.habitat_destino_id.is_full():
            raise ValidationError(_('El habitáculo de destino está lleno. No se pueden mover más animales.'))

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
            if not self.habitat_destino_id.is_full():
                animal.habitat_id = self.habitat_destino_id
            else:
                raise ValidationError(_('No se puede mover más animales al habitáculo de destino, está lleno.'))

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
            # Buscar todas las líneas de dieta para la especie y los alimentos seleccionados
            diet_lines = self.env['gestion_zoo.diet_line'].search([
                ('especie_id', '=', specie.id),
                ('food_id', 'in', self.food_ids.ids)  # Filtrar por los alimentos seleccionados
            ])
            
            if not diet_lines:
                raise ValidationError(f"No se encontraron líneas de dieta para la especie {specie.name} con los alimentos seleccionados.")
            
            # Eliminar las líneas de dieta que coinciden con los alimentos seleccionados
            diet_lines.unlink()

        # Mensaje de éxito, puedes personalizarlo o eliminarlo si prefieres solo cerrar el wizard
        return {
            'type': 'ir.actions.act_window_close'
        }
    
class AddContinentWizard(models.TransientModel):
    _name = 'gestion_zoo.add_continent_wizard'
    _description = 'Wizard para agregar continente a las especies seleccionadas'

    continent_ids = fields.Many2many('gestion_zoo.continente', string="Continentes", required=True)
    species_ids = fields.Many2many('gestion_zoo.especie', string='Especies', required=True)

    def action_add_continent(self):
        """Asocia el continente seleccionado a las especies seleccionadas, sin sobrescribir los existentes"""
        for species in self.species_ids:
            species.continent_ids |= self.continent_ids  # Agrega sin eliminar continentes existentes
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

        # Validación del límite de animales en el hábitat
        current_count = len(self.habitat_id.animal_ids)
        if self.number_of_animals + current_count > self.habitat_id.max_animals:
            raise ValidationError(_(
                'No se pueden añadir más animales. Capacidad máxima: %d, Actuales: %d, Intentando añadir: %d'
            ) % (self.habitat_id.max_animals, current_count, self.number_of_animals))

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

        return {
            'name': 'Animales Creados',
            'type': 'ir.actions.act_window',
            'res_model': 'gestion_zoo.animal',
            'domain': [('id', 'in', animal_ids)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    




class AlimentarAnimalesWizard(models.TransientModel):
    _name = 'gestion_zoo.alimentar_animales.wizard'
    _description = 'Wizard para alimentar animales en un hábitat'

    habitat_id = fields.Many2one('gestion_zoo.habitaculo', string='Habitáculo', required=True)
    start_date = fields.Date(string='Fecha de Inicio', required=True)
    end_date = fields.Date(string='Fecha de Fin', required=True)

    def feed_animals(self):
        # Verificar que las fechas son válidas
        if self.start_date > self.end_date:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Alerta",
                    'message': "La fecha inicial no debe ser mayor que la fecha final.",
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Obtener los animales del habitáculo seleccionado
        animals = self.habitat_id.animal_ids

        if not animals:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Información",
                    'message': "No hay animales en el habitaculo seleccionado.",
                    'type': 'info',
                    'sticky': False,
                }
            }

        # Convertir las fechas de inicio y fin
        current_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)

        # Contadores para seguimiento
        created_records = 0
        updated_records = 0

        # Iterar sobre cada día del rango
        while current_date <= end_date:
            for animal in animals:
                # Verificar si ya existe un registro de comida para este animal en la fecha actual
                existing_feed = self.env['gestion_zoo.comida_registro'].search([
                    ('animal_id', '=', animal.id),
                    ('fecha', '=', current_date)
                ])

                if existing_feed:
                    # Si ya existe el registro, actualizarlo con los valores de la dieta
                    if animal.species_id.diet_line_ids:
                        dieta = animal.species_id.diet_line_ids[0]  # Tomar la primera línea de dieta
                        existing_feed.write({
                            'tipo_comida_id': dieta.tipo_comida_id.id,
                            'cantidad': dieta.cantidad,
                        })
                        updated_records += 1
                else:
                    # Si no existe un registro, crearlo
                    if animal.species_id.diet_line_ids:
                        dieta = animal.species_id.diet_line_ids[0]  # Tomar la primera línea de dieta
                        self.env['gestion_zoo.comida_registro'].create({
                            'animal_id': animal.id,
                            'fecha': current_date,
                            'tipo_comida_id': dieta.tipo_comida_id.id,
                            'cantidad': dieta.cantidad,
                        })
                        created_records += 1
            
            # Avanzar al siguiente día
            current_date += timedelta(days=1)

        # Mensajes informativos
        if created_records > 0 or updated_records > 0:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Registros de comida actualizados.",
                    'message': (
                        f"Registros de comida creados: {created_records}. "
                        f"Registros de comida actualizados:: {updated_records}."
                    ),
                    'type': 'info',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Alerta",
                    'message': "Ningún registro de comida fue creado o actualizado.",
                    'type': 'warning',
                    'sticky': False,
                }
            }


class Empresa(models.Model):
    _name = 'gestion_zoo.empresa'  
    _description = 'Información de las empresas'  

    name = fields.Char(string='Empresa', required=True)
    address = fields.Text(string='Correo')
    continent_ids = fields.Many2many('gestion_zoo.continente', string='Continentes')
    phone = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo')
    website = fields.Char(string='Web')
    founded_date = fields.Date(string='Fecha de fundación')
    number_of_employees = fields.Integer(string='Nº Empleados')
    company_type = fields.Selection(
        [('pequeña', 'Pequeña'), ('mediana', 'Mediana'), ('larga', 'Larga')],
        string='Empresa',
        default='pequeña'
    )
    
    locales = fields.One2many(
        'gestion_zoo.local',  
        'empresa_id',         
        string='Locales'
    )
    
    total_employees = fields.Integer(string="Total de empleados", compute='_compute_total_employees', store=True)

    @api.depends('number_of_employees', 'locales.number_of_employees')
    def _compute_total_employees(self):
        for empresa in self:
            total_employees = empresa.number_of_employees
            for local in empresa.locales:
                total_employees += local.number_of_employees
            empresa.total_employees = total_employees

    def action_calcular_empleados(self):
        self._compute_total_employees()  # Corregido el nombre del método
        return {
            'type': 'ir.actions.act_window',
            'name': 'Total de Empleados',
            'res_model': 'gestion_zoo.wizard.total.empleados',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_empresa_id': self.id,
                'default_total_empleados': self.total_employees,
                'default_nombre_empresa': self.name,
            }
        }


class Local(models.Model):
    _name = 'gestion_zoo.local'  # Nombre técnico del modelo
    _description = 'Información de los locales'  # Descripción del modelo
    
    name = fields.Char(string='Nombre', required=True)
    address = fields.Text(string='Dirección')
    phone = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo')
    empresa_id = fields.Many2one('gestion_zoo.empresa', string='Empresa', ondelete='cascade')  # Relación con la empresa
    number_of_employees = fields.Integer(string='Nº Empleados')


class WizardTotalEmpleados(models.TransientModel):
    _name = 'gestion_zoo.wizard.total.empleados'
    _description = 'Wizard para mostrar total de empleados'

    empresa_id = fields.Many2one('gestion_zoo.empresa', string='Empresa')
    nombre_empresa = fields.Char(string='Nombre de la Empresa')
    total_empleados = fields.Integer(string='Total de Empleados')

class WizardEmpresasPorContinente(models.TransientModel):
    _name = 'gestion_zoo.wizard_empresas_por_continente'
    _description = 'Wizard para mostrar el número de empresas por continente'

    continente_id = fields.Many2one('gestion_zoo.continente', string='Continente', required=True)
    mensaje_empresas = fields.Char(string='Mensaje de Empresas', readonly=True)

    @api.onchange('continente_id')
    def _onchange_continente(self):
        """Calcula el número de empresas del continente seleccionado y lo muestra"""
        if self.continente_id:
            cantidad_empresas = len(self.continente_id.empresa_ids)
            self.mensaje_empresas = f'El continente "{self.continente_id.name}" tiene {cantidad_empresas} empresa(s).'
        else:
            self.mensaje_empresas = ''


    def action_cancel(self):
        """Método para cerrar el wizard"""
        return {'type': 'ir.actions.act_window_close'}

class WizardLocalesPorContinente(models.TransientModel):
    _name = 'gestion_zoo.wizard_locales_por_continente'
    _description = 'Wizard para mostrar el número total de locales por continente'

    continente_id = fields.Many2one('gestion_zoo.continente', string='Continente', required=True)
    mensaje_locales = fields.Char(string='Mensaje de Locales', readonly=True)

    @api.onchange('continente_id')
    def _onchange_continente(self):
        """Calcula el número total de locales del continente seleccionado y lo muestra"""
        if self.continente_id:
            cantidad_locales = 0
            for empresa in self.continente_id.empresa_ids:
                cantidad_locales += len(empresa.locales)
            self.mensaje_locales = f'El continente "{self.continente_id.name}" tiene {cantidad_locales} local(es).'
        else:
            self.mensaje_locales = ''

    def action_cancel(self):
        """Método para cerrar el wizard"""
        return {'type': 'ir.actions.act_window_close'}










