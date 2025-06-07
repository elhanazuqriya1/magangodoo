from odoo import models, fields

class Diagnosa(models.Model):
    _name = 'simrs.diagnosa'
    _description = 'Data Diagnosa'
    _rec_name = 'name'

    name = fields.Char(string="Nama Diagnosa", required=True)
    kode = fields.Char(string="Kode ICD-10", required=True, unique=True)
