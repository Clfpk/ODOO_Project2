from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    distribution_sample_product_ids = fields.One2many('distribute.sample.products', 'crm_lead_id', string='Sample Products')

    def action_create_picking(self):
        picking_obj = self.env['stock.picking']
        for lead in self:
            if not lead.distribution_sample_product_ids:
                continue
            picking = picking_obj.create({
                'partner_id': lead.partner_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,  # Default source location
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,  # Default destination location
                'picking_type_id': self.env.ref('stock.picking_type_out').id,
                'origin': lead.name,
                'move_lines': [(0, 0, {
                    'name': product.product_id.name,
                    'product_id': product.product_id.id,
                    'product_uom_qty': product.quantity,
                    'product_uom': product.product_id.uom_id.id,
                    'location_id': self.env.ref('stock.stock_location_stock').id,
                    'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                }) for product in lead.distribution_sample_product_ids],
            })
            picking.action_confirm()
            picking.action_assign()
