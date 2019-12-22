# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class ibas_indigo(models.Model):
#     _name = 'ibas_indigo.ibas_indigo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100