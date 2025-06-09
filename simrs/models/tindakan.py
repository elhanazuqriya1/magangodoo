from odoo import models, fields, api

class Tindakan(models.Model):
    _name = 'simrs.tindakan'
    _description = 'Data Tindakan Pasien'

    pasien_id = fields.Many2one('simrs.pasien', string="Pasien", required=True)
    unit_id = fields.Many2one('simrs.unit', string="Poli", required=True)  
    diagnosa_id = fields.Many2one('simrs.icd10', string="Diagnosa (ICD-10)", required=True)
    dokter_id = fields.Many2one('simrs.dokter', string="Dokter", required=True)
    tindakan_id = fields.Many2one('simrs.icd9', string="Prosedur (ICD-9)", required=True)
    catatan_id = fields.Text(string="Catatan Tambahan")

    @api.onchange('pasien_id')
    def _onchange_pasien_id(self):
        if self.pasien_id:
            unit_ids = self.env['simrs.pendaftaran'].search([
                ('pasien_id', '=', self.pasien_id.id)
            ]).mapped('unit_id').ids

            return {
                'domain': {
                    'unit_id': [('id', 'in', unit_ids)]
                }
            }
        else:
            return {
                'domain': {
                    'unit_id': []
                }
            }

    @api.onchange('unit_id')
    def _onchange_unit_id(self):
        if self.unit_id:
            return {
                'domain': {
                    'dokter_id': [('unit_id', '=', self.unit_id.id)]
                }
            }
        else:
            return {
                'domain': {
                    'dokter_id': []
                }
            }
