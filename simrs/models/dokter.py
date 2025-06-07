from odoo import models, fields

class Dokter(models.Model):
    _name = 'simrs.dokter'
    _description = 'Data Dokter'
    _rec_name = 'name'

    name = fields.Char(string="Nama Dokter", required=True)
    spesialis = fields.Char(string="Spesialisasi")
    unit_id = fields.Many2one('simrs.unit', string="Unit/Poli")
