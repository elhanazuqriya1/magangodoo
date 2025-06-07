from odoo import http
from odoo.http import request
import json

class SimrsController(http.Controller):

    # Route untuk halaman landing page
    @http.route('/landingpage', type='http', auth='public', website=True)
    def landing_page(self):
        # Render template untuk halaman utama
        return request.render('simrs.landing_page_template')

    # Route untuk menampilkan formulir pendaftaran (metode GET)
    @http.route('/pendaftaran', type='http', auth='public', methods=['GET'], website=True)
    def show_pendaftaran_form(self):
        # Render template untuk formulir pendaftaran
        return request.render('simrs.pendaftaran_template')

    # Route untuk menangani pengiriman formulir pendaftaran (metode POST)
    @http.route('/pendaftaran', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def pendaftaran(self, **post):
        # Mengambil data dari formulir
        name = post.get('name')
        tempat_lahir = post.get('tempat_lahir')
        dob = post.get('dob')
        gender = post.get('gender')
        goldar = post.get('goldar')
        phone = post.get('phone')
        alamat = post.get('alamat')
        
        # Membuat record pasien baru
        pasien = request.env['simrs.pasien'].create({
            'name': name,
            'tempat_lahir': tempat_lahir,
            'dob': dob,
            'gender': gender,
            'goldar': goldar,
            'phone': phone,
            'alamat': alamat,
        })
        
        # Menyimpan data pasien yang telah dibuat untuk ditampilkan di template sukses
        pasien_name = pasien.name
        no_rm = pasien.no_rm
        tempat_lahir = pasien.tempat_lahir
        pasien_dob = pasien.dob
        pasien_age = pasien.age
        pasien_gender = pasien.gender
        registration_date = pasien.registration_date
        
        # Render template sukses dengan data pasien
        return request.render('simrs.success_template', {
            'pasien_name': pasien_name,
            'no_rm': no_rm,
            'tempat_lahir': tempat_lahir,
            'pasien_dob': pasien_dob,
            'pasien_age_detail': pasien.get_age_detail(),
            'pasien_gender': pasien_gender,
            'registration_date': pasien.registration_date,
            'datetime_indonesia': pasien.datetime_indonesia,
        })

    # Route untuk halaman sukses setelah pendaftaran
    @http.route('/success_template', type='http', auth='public', website=True)
    def success_template(self):
        # Render template untuk halaman sukses
        return request.render('simrs.success_template')

    @http.route(['/pendaftaranpoli'], type='http', auth='public', website=True)
    def daftar_poli_form(self, **kw):
        pasien_list = request.env['simrs.pasien'].sudo().search([])
        unit_list = request.env['simrs.unit'].sudo().search([])
        from datetime import date
        return request.render('simrs.daftar_poli_template', {
            'pasien_list': pasien_list,
            'unit_list': unit_list,
            'default_date': date.today().strftime('%Y-%m-%d')
        })

    @http.route(['/pendaftaranpoli/sukses'], type='http', auth='public', website=True, csrf=False)
    def daftar_poli_sukses(self, **post):
        pendaftaran = request.env['simrs.pendaftaran'].sudo().create({
            'pasien_id': int(post.get('pasien_id')),
            'no_rm': post.get('no_rm'),
            'unit_id': int(post.get('unit_id')),
            'dokter_id': int(post.get('dokter_id')),
            'tanggal': post.get('tanggal'),
        })
        return request.render('simrs.daftar_poli_sukses_template', {
            'pendaftaran': pendaftaran
        })

    @http.route(['/pendaftaranpoli/berhasil'], type='http', auth='public', website=True)
    def daftar_sukses(self, **kw):
        return "<h2 style='text-align:center;margin-top:50px;'>Pendaftaran Poli Berhasil!</h2>"

    # Endpoint untuk ambil dokter berdasarkan unit
    @http.route('/get_dokter_by_unit/<int:unit_id>', type='http', auth='public', website=True)
    def get_dokter_by_unit(self, unit_id, **kwargs):
        dokter_list = request.env['simrs.dokter'].sudo().search([('unit_id', '=', unit_id)])
        result = [{'id': d.id, 'name': d.name} for d in dokter_list]
        return http.Response(
            json.dumps(result),
            content_type='application/json'
        )