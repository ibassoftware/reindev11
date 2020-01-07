# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from datetime import date

_logger = logging.getLogger(__name__)

class IBASStockMove(models.Model):
    _inherit = 'stock.move'

    price_before_lc = fields.Float(compute='_compute_price_before_lc', string='Unit Price before LC', store= True)
    value_before_lc = fields.Float(compute='_compute_price_before_lc', string='Value before LC', store= True)
    analytic_id = fields.Many2one('account.analytic.account', compute='_compute_price_before_lc', string='Analytic Account', store= True)

    stock_age = fields.Integer(compute='_compute_stock_age', string='Stock Age in Days')
    
    @api.depends('date')
    def _compute_stock_age(self):
        for rec in self:
            elapsed_delta = date.today() - fields.Datetime.from_string(rec.date).date()
            rec.stock_age = elapsed_delta.days
    
    
    @api.depends('landed_cost_value', 'value')
    def _compute_price_before_lc(self):
        for rec in self:
            if rec.purchase_line_id is not False:
                    rec.analytic_id = rec.purchase_line_id.account_analytic_id.id
            if rec.landed_cost_value > 0:
                rec.price_before_lc = (rec.value - rec.landed_cost_value) / rec.quantity_done
                rec.value_before_lc = rec.value - rec.landed_cost_value
    
