from odoo import fields, models


class OrderLineInherit(models.Model):
    _inherit = 'product.order.line'

    material_name = fields.Char(string='Material Name', required=True)
