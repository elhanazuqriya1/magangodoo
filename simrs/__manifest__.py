{
    "name": "SIMRS",
    "version": "1.0",
    "depends": ["base"],
    "data": [
        # Security
        "security/ir.model.access.csv",

        # Data
        "data/sequence.xml",

        # Reports
        "report/report_pendaftaran_pdf.xml",

        # Views
        "views/unit_views.xml",
        "views/diagnosa_views.xml",
        "views/icd10_views.xml",
        "views/icd9_views.xml",
        "views/dokter_views.xml",
        "views/pendaftaran_views.xml",
        "views/pasien_views.xml",
        "views/tindakan_views.xml",
        "views/menus.xml",

        # Templates
        "views/landing_page_template.xml",
        "views/pendaftaran_template.xml",
        "views/success_template.xml",
        "views/daftar_poli_template.xml",
        "views/daftar_poli_sukses_template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "simrs/static/src/css/styles.css",
            "simrs/static/src/css/login_custom.css",
        ],
        "web.assets_common": [
            "simrs/static/src/css/login_custom.css",
        ],
    },
    "installable": True,
    "application": True,
}
