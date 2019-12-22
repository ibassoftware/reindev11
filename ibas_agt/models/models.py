# -*- coding: utf-8 -*-

from odoo import models, fields, api

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