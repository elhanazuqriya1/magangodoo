from odoo import models, fields, api
from datetime import datetime, date
from calendar import monthrange
import logging
import pytz

_logger = logging.getLogger(__name__)

class Pasien(models.Model):
    _name = 'simrs.pasien'
    _description = 'Data Pasien'
    _rec_name = 'name'

    name = fields.Char(string="Nama Pasien", required=True)
    no_rm = fields.Char(string="No Rekam Medis", copy=False, index=True, readonly=True)
    dob = fields.Date(string="Tanggal Lahir")
    tempat_lahir = fields.Char(string="Tempat Lahir")  # New field for Place of Birth
    gender = fields.Selection([
        ('male', 'Laki-Laki'),
        ('female', 'Perempuan')
    ], string="Jenis Kelamin")
    age = fields.Integer(string="Umur", compute="_compute_age", store=True)
    goldar = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ], string="Golongan Darah")
    phone = fields.Char(string="Telepon")
    alamat = fields.Text(string="Alamat")
    registration_date = fields.Date(string="Tanggal Pendaftaran", default=fields.Date.context_today, required=True)

    # Field untuk tanggal & waktu Indonesia (real-time)
    datetime_indonesia = fields.Char(
        string="Tanggal & Waktu",
        compute="_compute_datetime_indonesia",
        store=False
    )

    _sql_constraints = [
        ('no_rm_unique', 'unique(no_rm)', 'Nomor Rekam Medis harus unik!')
    ]

    @api.depends('dob')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.dob:
                record.age = today.year - record.dob.year - ((today.month, today.day) < (record.dob.month, record.dob.day))
            else:
                record.age = False

    def get_age_detail(self):
        for record in self:
            if not record.dob:
                return "0 Tahun, 0 Bulan, 0 Hari"

            today = fields.Date.today()
            dob = record.dob

            years = today.year - dob.year
            months = today.month - dob.month
            days = today.day - dob.day

            if days < 0:
                months -= 1
                last_month = (today.month - 1) or 12
                year_of_last_month = today.year if today.month != 1 else today.year - 1
                days += monthrange(year_of_last_month, last_month)[1]

            if months < 0:
                years -= 1
                months += 12

            return f"{years} Tahun, {months} Bulan, {days} Hari"

    def get_datetime_indonesia(self):
        hari_map = {
            'Senin': 'Senin', 'Selasa': 'Selasa', 'Rabu': 'Rabu',
            'Kamis': 'Kamis', 'Jumat': 'Jumat', 'Sabtu': 'Sabtu', 'Minggu': 'Minggu',
            'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
            'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
        }
        bulan_map = {
            'January': 'Januari', 'February': 'Februari', 'March': 'Maret', 'April': 'April',
            'May': 'Mei', 'June': 'Juni', 'July': 'Juli', 'August': 'Agustus',
            'September': 'September', 'October': 'Oktober', 'November': 'November', 'December': 'Desember'
        }
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(tz)
        hari = hari_map.get(now.strftime('%A'), now.strftime('%A'))
        bulan = bulan_map.get(now.strftime('%B'), now.strftime('%B'))
        return f"{hari}, {now.strftime('%d')} {bulan} {now.strftime('%Y %H:%M:%S')}"

    def _compute_datetime_indonesia(self):
        for record in self:
            record.datetime_indonesia = record.get_datetime_indonesia()

    @api.model
    def create(self, vals):
        if 'no_rm' not in vals or not vals.get('no_rm'):
            # Ambil tanggal pendaftaran atau hari ini
            tanggal_daftar = vals.get('registration_date') or fields.Date.context_today(self)

            # Konversi ke date jika berupa string
            if isinstance(tanggal_daftar, str):
                try:
                    tanggal_daftar = fields.Date.to_date(tanggal_daftar)
                except Exception as e:
                    _logger.error("Gagal parsing tanggal_daftar: %s", e)
                    raise ValueError("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")

            # Validasi tipe akhir
            if not isinstance(tanggal_daftar, date):
                raise ValueError("Field 'registration_date' harus berupa date, bukan string.")

            # Format nomor RM: RM-mmYY-0001 (dengan tanda strip)
            bulan = tanggal_daftar.strftime("%m")
            tahun = tanggal_daftar.strftime("%y")
            tanggal_str = f"{bulan}{tahun}"
            
            domain = [('registration_date', '=', tanggal_daftar)]
            jumlah_pasien = self.search_count(domain)
            urut = jumlah_pasien + 1

            vals['no_rm'] = f"RM-{tanggal_str}-{urut:04d}"

        # Default registration_date jika tidak ada
        if 'registration_date' not in vals:
            vals['registration_date'] = fields.Date.context_today(self)

        return super(Pasien, self).create(vals)