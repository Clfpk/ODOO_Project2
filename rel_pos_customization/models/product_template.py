# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timezone
import pytz
from pytz import timezone, UTC, utc
from typing import List, Tuple

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ProductTemplaye(models.Model):
    _inherit = "product.template"

    image_test = fields.Char()

