from odoo import models, fields, api

class AutoValidatePickingWizard(models.TransientModel):
    _name = 'auto.validate.picking.wizard'
    _description = 'Auto Validate Picking Wizard'

    sample_order_ids = fields.Many2many('distribution.sample.order', string='Sample Orders')

    def action_validate(self):
        for order in self.sample_order_ids:
            order.action_create_picking()
        return {'type': 'ir.actions.act_window_close'}
