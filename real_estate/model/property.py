from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class realestate(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'
    _order = "name "

    name = fields.Char(string='Name', size=40)
    bedrooms = fields.Integer(string='Bedroom')
    living_area = fields.Integer(string='Living_area')
    facades = fields.Integer(string='Facades')
    country = fields.Many2one('res.country', string='Country')
    description = fields.Char(string='Description', size=100)
    postcode = fields.Char(string="Postcode")
    selling_price = fields.Float(string="Selling_Price")
    mob = fields.Char(string='Contact_Num', required=True)
    email = fields.Char(string='Email', required=True)
    garden = fields.Boolean(string="Garden")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('east', 'East'),
            ('west', 'West'),
            ('south', 'South')
        ],
        string="garden_orientation")
    creation_date = fields.Datetime(string="Creation_Date", default=fields.Datetime.now)
    property_owner = fields.One2many('estate.property.type', 'property_types_id', string='Property Owner')
    buyer = fields.One2many('estate.property.type', 'buyer', string='Buyer')
    property_types_id = fields.Selection(selection=[
        ('home', 'Home'),
        ('villa', 'Villa'),
        ('flat', 'Flat'),
        ('farm', 'Farm')
    ],
        string='Property Types')

    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    computed_fields = fields.Float(string="Garden area", compute="_compute_computed_fields")

    @api.depends('length', 'width')
    def _compute_computed_fields(self):
        for record in self:
            record.computed_fields = record.length * record.width

    def action_reset(self):
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not tools.float_is_zero(record.selling_price, precision_digits=2):
                raise ValidationError("Selling price cannot be in minus!")

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'email must be unique!')
    ]

    _sql_constraints = [
        ('mob_unique', 'unique(mob)', 'mob must be unique!')
    ]
