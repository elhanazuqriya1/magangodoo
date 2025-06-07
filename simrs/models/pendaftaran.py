from odoo import models, fields, api
from datetime import datetime

class Pendaftaran(models.Model):
    _name = 'simrs.pendaftaran'
    _description = 'Data Pendaftaran'
    _rec_name = 'nomor_antrian'

    name = fields.Char(string="No Pendaftaran", required=True, copy=False, readonly=True)
    no_rm = fields.Char(string="No RM", readonly=True)
    nomor_antrian = fields.Char(string="Nomor Antrian", readonly=True, copy=False)
    pasien_id = fields.Many2one('simrs.pasien', string="Pasien", required=True)
    unit_id = fields.Many2one('simrs.unit', string="Poli/Unit", required=True)
    dokter_id = fields.Many2one('simrs.dokter', string="Dokter")
    tanggal = fields.Date(string="Tanggal", default=fields.Date.context_today, required=True)

    @api.model
    def create(self, vals):
        # 1. Tanggal Daftar
        tanggal = vals.get('tanggal') or fields.Date.context_today(self)
        tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d")
        tanggal_str = tanggal_obj.strftime("%d%m%y")

        #no_rm otomatis
        pasien = self.env['simrs.pasien'].browse(vals.get('pasien_id'))
        vals['no_rm'] = pasien.no_rm if pasien else ''

        # 2. Nomor Pendaftaran: PDN-ddmmyy-XXX
        count_today = self.search_count([('tanggal', '=', tanggal)])
        nomor_urut = count_today + 1
        vals['name'] = f"PDN-{tanggal_str}-{nomor_urut:03d}"

        # 3. Nomor Antrian berdasarkan Unit
        unit = self.env['simrs.unit'].browse(vals.get('unit_id'))
        if unit and unit.kode:
            # Ambil antrian terakhir untuk unit & tanggal
            last_antrian = self.search([
                ('unit_id', '=', unit.id),
                ('tanggal', '=', tanggal)
            ], order="id desc", limit=1)

            if last_antrian and last_antrian.nomor_antrian:
                try:
                    last_number = int(last_antrian.nomor_antrian.split('-')[-1])
                except (IndexError, ValueError):
                    last_number = 0
            else:
                last_number = 0

            antrian_baru = last_number + 1
            vals['nomor_antrian'] = f"{unit.kode}-{antrian_baru:03d}"

        return super(Pendaftaran, self).create(vals)
