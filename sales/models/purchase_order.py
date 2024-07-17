from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    receipt_status = fields.Selection([
        ('nothing', 'Nothing to Receive'),
        ('to_receive', 'To Receive'),
        ('partial', 'Partially Received'),
        ('received', 'Received'),
        ('processing', 'Processing'),
    ], string='Receipt Status',compute='_compute_receipt_status', store=True)

    @api.depends('state', 'order_line.product_qty', 'order_line.qty_received')
    def _compute_receipt_status(self):
        for order in self:
            if order.state in ['purchase', 'done']:
                received_qty = sum(order.order_line.mapped('qty_received'))
                if received_qty == 0:
                    order.receipt_status = 'nothing'
                elif received_qty < sum(order.order_line.mapped('product_qty')):
                    order.receipt_status = 'partial'
                elif received_qty == sum(order.order_line.mapped('product_qty')):
                    order.receipt_status = 'received'
                else:
                    order.receipt_status = 'processing'
            else:
                order.receipt_status = 'to_receive'
