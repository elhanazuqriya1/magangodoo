from odoo import models, fields

class Unit(models.Model):
    _name = 'simrs.unit'
    _description = 'Data Unit/Poli'
    _rec_name = 'name'

    name = fields.Char(string="Nama Poli/Unit", required=True)
    kode = fields.Char(string="Kode Poli", required=True, unique=True)

