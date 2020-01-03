# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import date


_logger = logging.getLogger(__name__)   


class IBASAGTRecon(models.Model):
    _inherit = 'account.bank.statement'

    def ibas_unreconciled_get(self):
        for rec in self:
            lines = self.env['account.move.line'].search([("account_id.id","=",rec.journal_id.default_debit_account_id.id),
            ("statement_id","=",False)])

            for l in lines:
                if l.debit == 0:
                    myamount = l.credit * -1
                else:
                    myamount = l.debit 
                self.env["account.bank.statement.line"].create({
                    'statement_id': rec.id,
                    'date': l.date,
                    'name': l.name,
                    'partner_id': l.partner_id.id,
                    'amount': myamount
                })

class StockAgeWizard(models.TransientModel):
    _name = 'ibas_agt.stock_age.report'
    
    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {},
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('ibas_agt.recap_report').report_action(self, data=data)

class ReportStockAge(models.AbstractModel):
    _name = 'report.ibas_agt.stock_ageing_report'

    @api.model
    def get_report_values(self, docids, data=None):
        
        docs = []
        stock_moves = self.env['stock.move'].search([('remaining_qty','>',0)])
        for move in stock_moves:
            elapsed_delta = date.today() - fields.Datetime.from_string(move.date).date()
            analytic_tag = "none"
            if (move.purchase_line_id):
                if (move.purchase_line_id.account_analytic_id):
                    analytic_tag = move.purchase_line_id.account_analytic_id.name

            docs.append({
                'product': move.product_id.name,
                'analytic': analytic_tag,
                'quantity': move.remaining_qty,
                'value': move.remaining_value,
                'days': elapsed_delta.days
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'docs': docs,
        }



# class ibas_agt(models.Model):
#     _name = 'ibas_agt.ibas_agt'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100