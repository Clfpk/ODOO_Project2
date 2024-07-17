# -*- coding: utf-8 -*-

from functools import partial
from datetime import datetime, timezone
import pytz
from odoo import models, fields, api


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    table_id = fields.Many2one('restaurant.table', string='Floor', readonly=True)
    order_hour = fields.Integer('Hour')

    def _select(self):
        return super(PosOrderReport, self)._select() + ',s.table_id AS table_id ,s.order_hour AS order_hour'

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ',s.table_id, s.order_hour'

