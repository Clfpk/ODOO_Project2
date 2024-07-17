from odoo import api, fields, models


class EstateProperty(models.Model):

    _name = 'estate.property.type'
    _description = 'Types of Estate Property'

    property_owner = fields.Many2one('real.estate.property', string='Property Owwner')
    buyer = fields.Many2one('real.estate.property',string='Buyer')
    property_types_id = fields.Selection(selection=[
        ('home', 'Home'),
        ('villa', 'Villa'),
        ('flat', 'Flat'),
        ('farm', 'Farm')
        ],
        string='Property Types',related='property_owner.property_types_id')
    selling_price = fields.Float(string="Selling_Price",related='property_owner.selling_price')
    mob = fields.Char(string='Contact_Num')
    email = fields.Char(string='Email')
    state = fields.Selection([
        ('new', 'New'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold')
    ], string='State',default="new", required=True)
    selling_date = fields.Datetime(string="Selling Date", default=fields.Datetime.now)

    @api.onchange('property_owner')
    def onchange_property_owner(self):
        self.mob=self.property_owner.mob
        self.email = self.property_owner.email

    # def action_sold(self):
    #     self.action_sold()
    #     return {'type': 'ir.actions.client',
    #             'tag': 'sold'}

    def action_cancel(self):
        self.action_cancel()
        return {'type':'ir.actions.act_window',
                'tag':'reload'}

    def action_offer_accept(self):
        for record in self:
            record.state="offer_accepted"


    def action_sold(self):
        for record in self:
            record.state="sold"
