{
    "name": "Barcode Order Line",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "summary": "Agregar productos al pedido mediante escaneo de códigos de barras usando la cámara",
    "author": "Angel Barbero / Ecotisa ",
    "license": "AGPL-3",
    "depends": ["sale","stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/barcode_scan_wizard_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "views/assets.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js", 
            "barcode_order_line/static/src/js/barcode_scanner.js",
            
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
