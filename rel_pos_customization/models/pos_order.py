# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timezone
import pytz
from pytz import timezone, UTC, utc
from typing import List, Tuple

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class PosOrder(models.Model):
    _inherit = "pos.order"

    order_hour = fields.Integer(string='Order Hour', compute='_compute_order_hour', store=True)
    margin = fields.Monetary(string="Margin", compute='_compute_margin', store=True)
    margin_percent = fields.Float(string="Margin (%)", compute='_compute_margin', digits=(12, 4), store=True)

    @api.depends('date_order')  # Replace 'date_field' with your actual field
    def _compute_order_hour(self):
        for record in self:
            if record.date_order:
                tz = self.env.user.tz or pytz.utc
                last_datetime = record.date_order.replace(tzinfo=UTC).astimezone().replace(tzinfo=None)
                record.order_hour = last_datetime.hour
            else:
                record.order_hour = None


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    margin = fields.Monetary(string="Margin", compute='_compute_margin', store=True)
    margin_percent = fields.Float(string="Margin (%)", compute='_compute_margin', digits=(12, 4), store=True)
